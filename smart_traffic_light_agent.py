import mesa
import random
import math
from good_driver_agent import GoodDriverAgent

class SmartTrafficLightAgent(mesa.Agent):
    def __init__(self, unique_id, model, value, direction, color = False):
        super().__init__(unique_id, model)
        self.color = color
        self.value = value
        self.direction = direction
        self.priority = math.inf
        self.queue = []
        self.id = unique_id

    def turnOn (self, intersectionLight):
        intersectionLight.changeStatus('red')
        self.changeStatus('green')
        
    def calculatePriority (self):
        self.priority = math.inf
        agents = self.model.schedule.agents
        sameDirectionLight = list(filter(lambda agent: type(agent) == SmartTrafficLightAgent and agent.direction == self.direction and agent != self, agents))[0]
        intersectionLight = list(filter(lambda agent: type(agent) == SmartTrafficLightAgent and agent.direction != self.direction and agent.pos[1] < 19 and agent.pos[0] < 19, agents))[0]

        totalPrioritySum = 0     # Calculate priority with sum of vehicles
        for agent in self.queue:
            totalPrioritySum += agent[1]
        if totalPrioritySum > 0: self.priority = totalPrioritySum

        if len(self.queue) < 4:     # Use ETA if there are no more than 3 cars in line
            if self.priority < intersectionLight.priority: # My cars are closer
                self.turnOn(intersectionLight)
            elif self.priority == intersectionLight.priority and (not self.queue and intersectionLight.queue):
                randomLight = random.randrange(1, 2, 1)
                if (randomLight < 2):
                    self.turnOn(intersectionLight)
                else:
                    intersectionLight.turnOn(sameDirectionLight)
        elif len(self.queue) > len(intersectionLight.queue):
            self.turnOn(intersectionLight)

    def changeStatus(self, color):
        agents = self.model.schedule.agents
        sameDirectionLight = list(filter(lambda agent: type(agent) == SmartTrafficLightAgent and agent.direction == self.direction and agent != self, agents))[0]
        self.color = color
        sameDirectionLight.color = color

    def addCarToQueue (self, agent, ETA):
        self.queue.append((agent, ETA))
    
    def checkRoad(self):
        x,y = self.pos
        cellRange = []
        self.queue = []
        if self.direction == "north":
            for cell in range(1, 9):
                cellRange.append((x, y - cell))
        if self.direction == "east":
            for cell in range(1, 9):
                cellRange.append((x - cell, y))

        matesInCellPosition = self.model.grid.get_cell_list_contents(cellRange)

        for agentIndex in range(0, len(matesInCellPosition)):
            agent = matesInCellPosition[agentIndex]
            if type(agent) == GoodDriverAgent:
                if self.direction == "north":
                    _, agentY = agent.pos
                    self.addCarToQueue(agent, (agent.velocity * (self.pos[1] - agentY)))
                if self.direction == "east":
                    agentX, _ = agent.pos
                    self.addCarToQueue(agent, (agent.velocity * (self.pos[0] - agentX)))
            
    def step(self):
        self.checkRoad()
        self.calculatePriority()

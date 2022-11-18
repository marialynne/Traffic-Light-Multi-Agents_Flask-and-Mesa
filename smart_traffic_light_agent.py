import mesa
import random
import math
from good_driver_agent import GoodDriverAgent

class SmartTrafficLightAgent(mesa.Agent):
    def __init__(self, unique_id, model, layerLevel, scanRangeNumber, direction, letter, color = False):
        super().__init__(unique_id, model)
        self.layerLevel = layerLevel
        self.scanRangeNumber = scanRangeNumber
        self.direction = direction
        self.letter = letter
        self.color = color
        self.priority = math.inf
        self.queue = []

    """ def changeStatus(self, color):
        agents = self.model.schedule.agents
        sameDirectionLight = list(filter(lambda agent: type(agent) == SmartTrafficLightAgent and agent.direction == self.direction and agent != self, agents))[0]
        self.color = color
        sameDirectionLight.color = color
        
    def turnOn (self, intersectionLight):
        intersectionLight.changeStatus('red')
        self.changeStatus('green')
        
    """
    
    """ def calculatePriority (self):
        self.priority = math.inf
        agents = self.model.schedule.agents
        northDirectionLight = list(filter(lambda agent: type(agent) == SmartTrafficLightAgent and agent.direction == "north" and agent != self, agents))[0]
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
            self.turnOn(intersectionLight)  """


    def addCarToQueue (self, agent, ETA):
        self.queue.append((agent, ETA))
    
    
    def checkRoad(self):
        x,y = self.pos
        cellRange = []
        self.queue = []
        for cell in range(1, self.scanRangeNumber):
            if self.direction == "north": cellRange.append((x, y - cell))
            elif self.direction == "east": cellRange.append((x - cell, y))
            elif self.direction == "south": cellRange.append((x, y + cell))
            elif self.direction == "west": cellRange.append((x + cell, y))
            
        matesInCellPosition = self.model.grid.get_cell_list_contents(cellRange)
        
        for agentIndex in range(0, len(matesInCellPosition)):
            agent = matesInCellPosition[agentIndex]
            if type(agent) == GoodDriverAgent:
                agentX,agentY = agent.pos
                if self.direction == "north": self.addCarToQueue(agent, (agent.velocity * (self.pos[1] - agentY))) # Revisar bien orientacion
                elif self.direction == "east": self.addCarToQueue(agent, (agent.velocity * (self.pos[0] - agentX)))
                elif self.direction == "south": self.addCarToQueue(agent, (agent.velocity * (agentY - self.pos[1])))
                elif self.direction == "west": self.addCarToQueue(agent, (agent.velocity * (agentX - self.pos[0])))
            
            
    def step(self):
        self.checkRoad()
        #self.calculatePriority()

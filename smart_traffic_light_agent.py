import mesa
from good_driver_agent import GoodDriverAgent

class SmartTrafficLightAgent(mesa.Agent):
    def __init__(self, unique_id, model, value, direction, color, mainLight = False):
        super().__init__(unique_id, model)
        self.color = color
        self.value = value
        self.direction = direction
        self.priority = 0
        self.queue = []
        self.id = unique_id
        self.mainLight = False

    def turnOn (self, intersectionLight, sameDirectionLight):
        intersectionLight.changeStatus('red')
        self.changeStatus('green')
        sameDirectionLight.changeStatus('green')
        
    def calculatePriority (self):
        agents = self.model.schedule.agents
        sameDirectionLight = list(filter(lambda agent: type(agent) == SmartTrafficLightAgent and agent.direction == self.direction and agent != self, agents))[0]
        intersectionLight = list(filter(lambda agent: type(agent) == SmartTrafficLightAgent and agent.direction != self.direction and agent.pos[1] < 19 and agent.pos[0] < 19, agents))[0]

        if len(self.queue) <= 4:     # If I have less or eq to 4 cars waiting
            totalPrioritySum = 0     # Calculate priority with sum of vehicles
            for agent in self.queue:
                print(agent[1])
                totalPrioritySum += agent[1]
            self.priority = totalPrioritySum
        elif len(intersectionLight > 4):   # If the other light has more cars in queue priority is my qty of cars
            self.priority = len(self.queue)

        if intersectionLight.priority < self.priority and intersectionLight.priority < sameDirectionLight.priority:
            self.turnOn(intersectionLight, sameDirectionLight)
        
        # if self.color == 'yellow': self.turnOn(intersectionLight, sameDirectionLight) 
        
    def changeStatus(self, color):
        self.color = color

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
                    self.addCarToQueue(agent, (agent.velocity * (self.pos[1] - 1 - agentY)))
                if self.direction == "east":
                    agentX, _ = agent.pos
                    self.addCarToQueue(agent, (agent.velocity * (self.pos[0] - 1 - agentX)))
            
    def step(self):
        print(self.queue)
        self.checkRoad()
        self.calculatePriority()

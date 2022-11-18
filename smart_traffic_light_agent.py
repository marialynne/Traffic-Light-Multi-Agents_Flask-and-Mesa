import mesa
import math
from driver_agent import DriverAgent

class SmartTrafficLightAgent(mesa.Agent):
    def __init__(self, unique_id, model, layerLevel, scanRangeNumber, direction, color = "yellow"):
        super().__init__(unique_id, model)
        self.layerLevel = layerLevel
        self.scanRangeNumber = scanRangeNumber
        self.direction = direction
        self.color = color
        self.priority = math.inf
        self.queue = []

    def changeStatus(self, color):
        self.color = color
        
    def calculatePriority(self):
        self.priority = math.inf
        totalPrioritySum = 0
        for agent in self.queue:
            totalPrioritySum += agent[1]
        if totalPrioritySum > 0: self.priority = totalPrioritySum

    def addCarToQueue (self, agent, ETA):
        self.queue.append((agent, ETA))

    def checkRoad(self):
        x,y = self.pos
        cellRange = []
        self.queue = []
        for cell in range(0, self.scanRangeNumber):
            if self.direction == "north": cellRange.append((x, y - cell))
            elif self.direction == "east": cellRange.append((x - cell, y))
            elif self.direction == "south": cellRange.append((x, y + cell))
            elif self.direction == "west": cellRange.append((x + cell, y))

        matesInCellPosition = self.model.grid.get_cell_list_contents(cellRange)
        
        for agentIndex in range(0, len(matesInCellPosition)):
            agent = matesInCellPosition[agentIndex]
            if type(agent) == DriverAgent:
                agentX,agentY = agent.pos
                if self.direction == "north": self.addCarToQueue(agent, (agent.velocity * (self.pos[1] - agentY))) # Revisar bien orientacion
                elif self.direction == "east": self.addCarToQueue(agent, (agent.velocity * (self.pos[0] - agentX)))
                elif self.direction == "south": self.addCarToQueue(agent, (agent.velocity * (agentY - self.pos[1])))
                elif self.direction == "west": self.addCarToQueue(agent, (agent.velocity * (agentX - self.pos[0])))
            
    def step(self):
        self.checkRoad()
        self.calculatePriority()

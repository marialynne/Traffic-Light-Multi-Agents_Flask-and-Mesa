import mesa
import math
from driver_agent import DriverAgent

class SmartTrafficLightAgent(mesa.Agent):
    def __init__(self, unique_id, model, scanRangeNumber, direction, color = "yellow", layerLevel = 2):
        super().__init__(unique_id, model)
        self.layerLevel = layerLevel
        self.scanRangeNumber = scanRangeNumber
        self.direction = direction
        self.color = color
        self.congestion = 0
        self.queue = []
        self.firstETA = math.inf
    
    def changeStatus(self, color) -> None:
        self.color = color
        
    def getFirstETA(self) -> None:
        if(len(self.queue) > 0): 
            agent = self.queue[0]
            self.firstETA = agent[1]
        else: self.firstETA = math.inf
        
    def calculateCongestion(self) -> None:
        self.congestion = len(self.queue) 

    def addCarToQueue (self, agent, ETA) -> None:
        self.queue.append((agent, ETA))

    def checkRoad(self) -> None:
        x,y = self.pos
        cellRange = []
        self.queue = []
        for cell in range(0, self.scanRangeNumber):
            if self.direction == "north": cellRange.append((x, y - cell))
            elif self.direction == "east": cellRange.append((x - cell, y))
            elif self.direction == "south": cellRange.append((x, y + cell))
            elif self.direction == "west": cellRange.append((x + cell, y))
        # Get all Agents on traffic light radar
        matesInCellPosition = self.model.grid.get_cell_list_contents(cellRange)
        # Save the cars in a list, together with their estimated arrival time (ETA)
        for agentIndex in range(0, len(matesInCellPosition)):
            agent = matesInCellPosition[agentIndex]
            if type(agent) == DriverAgent:
                agentX,agentY = agent.pos
                if self.direction == "north": self.addCarToQueue(agent, (agent.velocity * (self.pos[1] - agentY)))
                elif self.direction == "east": self.addCarToQueue(agent, (agent.velocity * (self.pos[0] - agentX)))
                elif self.direction == "south": self.addCarToQueue(agent, (agent.velocity * (agentY - self.pos[1])))
                elif self.direction == "west": self.addCarToQueue(agent, (agent.velocity * (agentX - self.pos[0])))
            
    def step(self) -> None:
        self.checkRoad() # Get agents on road
        self.calculateCongestion() # Get congestion on road
        self.getFirstETA() # Gets first eta of agent on road


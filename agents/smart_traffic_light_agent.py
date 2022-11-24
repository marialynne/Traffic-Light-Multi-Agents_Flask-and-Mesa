import mesa
import math


class SmartTrafficLightAgent(mesa.Agent):
    def __init__(self, unique_id, model, scanRangeNumber, direction, driversSample, color="yellow", layerLevel=2):
        super().__init__(unique_id, model)
        self.layerLevel = layerLevel
        self.scanRangeNumber = scanRangeNumber
        self.direction = direction
        self.color = color
        self.congestion = 0
        self.queue = []
        self.firstETA = math.inf
        self.hasAnAmbulance = False
        self.driversSample = driversSample

    def changeStatus(self, color) -> None:
        self.color = color

    def getFirstETA(self) -> None:
        if (len(self.queue) > 0):
            driver = self.queue[0]
            self.firstETA = driver[1]
        else:
            self.firstETA = math.inf

    def calculateCongestion(self) -> None:
        self.congestion = len(self.queue)

    def searchAmbulance(self, matesInCellPosition) -> bool:
        for agentIndex in range(0, len(matesInCellPosition)):
            agent = matesInCellPosition[agentIndex]
            return [type(agent) == type(self.driversSample) and agent.isPriority]

    def addCarToQueue(self, matesInCellPosition) -> None:
        # Save the cars in a list, together with their estimated arrival time (ETA)
        for agentIndex in range(0, len(matesInCellPosition)):
            agent = matesInCellPosition[agentIndex]
            if type(agent) == type(self.driversSample):
                agentX, agentY = agent.pos
                if self.direction == "north":
                    self.queue.append(
                        (agent, (agent.velocity * (self.pos[1] - agentY))))
                elif self.direction == "east":
                    self.queue.append(
                        (agent, (agent.velocity * (self.pos[0] - agentX))))
                elif self.direction == "south":
                    self.queue.append(
                        (agent, (agent.velocity * (agentY - self.pos[1]))))
                elif self.direction == "west":
                    self.queue.append(
                        (agent, (agent.velocity * (agentX - self.pos[0]))))

    def checkRoad(self) -> None:
        x, y = self.pos
        cellRange = []
        self.queue = []
        for cell in range(0, self.scanRangeNumber):
            if self.direction == "north":
                cellRange.append((x, y - cell))
            elif self.direction == "east":
                cellRange.append((x - cell, y))
            elif self.direction == "south":
                cellRange.append((x, y + cell))
            elif self.direction == "west":
                cellRange.append((x + cell, y))
        # Get all Agents on traffic light radar
        matesInCellPosition = self.model.grid.get_cell_list_contents(cellRange)
        # Add drivres to queue
        self.addCarToQueue(matesInCellPosition)
        # Search for an ambulance in the queue
        if (self.searchAmbulance(matesInCellPosition)):
            self.hasAnAmbulance = True
        else:
            self.hasAnAmbulance = False

    def step(self) -> None:
        self.checkRoad()  # Check the road for drivers or ambulances
        self.calculateCongestion()  # Get congestion on road
        self.getFirstETA()  # Gets first eta of agent on road

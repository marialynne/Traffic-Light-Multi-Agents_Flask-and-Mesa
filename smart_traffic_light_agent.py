import mesa
import math
#from driver_agent import DriverAgent
from road_agent import RoadAgent

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

    def returnStatus(self):
        return self.color
        
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

class DriverAgent(mesa.Agent):
    def __init__(self, unique_id, model, layerLevel, velocity):
        super().__init__(unique_id, model)
        self.layerLevel = layerLevel
        self.velocity = velocity
        self.priority = 1
        
    # Funcion que determina que debe para cuando exista un coche adelante
    def stopCar(self, agent):
        next_position = self.getNextPosition(agent)
        cellmates = self.model.grid.get_cell_list_contents([next_position])
        nextCellDrivers = 0
        TraficLightStatus = True
        for agent in cellmates: 
            #print("agent ",type(agent))
            if type(agent) == DriverAgent: #If there is a car in front of current Agent
                nextCellDrivers += 1
            elif type(agent) == SmartTrafficLightAgent:
                if(agent.returnStatus() == "red"): #If the trafic Light is currently red
                    TraficLightStatus = False
        if nextCellDrivers >= 1 or not TraficLightStatus:
            return False
        else:
            return True

    # Funcion que detiene el vehiculo cuando la siguiente casilla sea un semaforo y este en rojo
    
    # Funcion que detecte si el camino del frente es posible punto de colision, entonces, ya no se detiene si hay cochec al frente
    def continueIfColissionPoint(self, agent):
        next_position = self.getNextPosition(agent)
        if(next_position == [10, 10] or next_position == [10, 20] or next_position == [20, 10]):
            return True
        else:
            return False

    # ya no hara falta crear mucho tipos de coches
    
    def getNextPosition(self, agent):
        if len(agent.directions) > 1:
            direction = self.random.choice(agent.directions) 
        if len(agent.directions) == 1:
            direction = agent.directions[0]
        x,y = self.pos
        if direction == "north": return(x,y+1)
        if direction == "south": return(x,y-1)
        if direction == "west": return(x-1,y)
        if direction == "east": return(x+1,y) 

    def move(self):
        cellmates = self.model.grid.get_cell_list_contents([self.pos])
        for agent in cellmates: 
            if type(agent) == RoadAgent and (self.stopCar(agent) or self.continueIfColissionPoint(agent)):
                new_position = self.getNextPosition(agent)
                self.model.grid.move_agent(self, new_position)
                 
    def step(self):
        self.move() 


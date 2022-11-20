import mesa
from road_agent import RoadAgent
from intersection_traffic_lights import IntersectionTrafficLightsAgent
from smart_traffic_light_agent import SmartTrafficLightAgent

class DriverAgent(mesa.Agent):
    def __init__(self, unique_id, model, driverType, layerLevel = 1):
        super().__init__(unique_id, model)
        self.layerLevel = layerLevel
        self.velocityIndex = 0
        self.driverType = driverType
        # Los siguientes se modifican segun el driver
        self.velocity = 2
        self.isPriority = False # Ambulance
        self.sanity = 0
    
    def getNextPosition(self, agent) -> None:
        if len(agent.directions) > 1:
            direction = self.random.choice(agent.directions) 
        if len(agent.directions) == 1:
            direction = agent.directions[0]
        x,y = self.pos
        if direction == "north": return(x,y+1)
        elif direction == "south": return(x,y-1)
        elif direction == "west": return(x-1,y)
        elif direction == "east": return(x+1,y) 
    
    def move(self) -> None:
        if (self.velocityIndex < self.velocity):
            self.velocityIndex += 1
        if(self.velocityIndex == self.velocity):
            cellmates = self.model.grid.get_cell_list_contents([self.pos]) # Gets all the agents on road
            newPosition = self.checkMovement(cellmates)
            self.model.grid.move_agent(self,newPosition)
            self.velocityIndex = 0
            
    def checkMovement(self, cellmates) -> tuple:
        for agent in cellmates:
            newMoveMates = self.model.grid.get_cell_list_contents([self.getNextPosition(agent)])
            for newAgent in newMoveMates:
                if(type(newAgent) == SmartTrafficLightAgent and newAgent.color == "red"):
                    return (self.pos)
                elif (type(newAgent) == DriverAgent) and (type(newAgent) != IntersectionTrafficLightsAgent):
                    return (self.pos)
            if type(agent) == RoadAgent:
                return self.getNextPosition(agent)
                          
    def step(self) -> None:
        self.move() 

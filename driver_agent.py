import mesa
from road_agent import RoadAgent
from intersection_traffic_lights import IntersectionTrafficLightsAgent
from smart_traffic_light_agent import SmartTrafficLightAgent

class DriverAgent(mesa.Agent):
    def __init__(self, unique_id, model, velocity, driverType, layerLevel = 1):
        super().__init__(unique_id, model)
        self.layerLevel = layerLevel
        self.velocity = velocity
        self.isPriority = False
        self.driverType = driverType
        
    def isGreen(self, newPosition) -> bool:
        cellmates = self.model.grid.get_cell_list_contents([newPosition])
        for agent in cellmates: 
            if type(agent) == SmartTrafficLightAgent:
                return True
            else: 
                return False
            
    # Funcion que determina que debe para cuando exista un coche adelante
    def noCarInFront(self, newPosition) -> bool:
        cellmates = self.model.grid.get_cell_list_contents([newPosition])
        for agent in cellmates: 
            return [(type(agent) != DriverAgent)] 
            
    # Funcion que detecte si el camino del frente es posible punto de colision, entonces, ya no se detiene si hay cochec al frente
    def continueIfColissionPoint(self, newPosition) -> bool:
        cellmates = self.model.grid.get_cell_list_contents([newPosition])
        for agent in cellmates:
            if(type(agent) == IntersectionTrafficLightsAgent):
                return True
            else:
                return False
    
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
        cellmates = self.model.grid.get_cell_list_contents([self.pos]) # Gets all the road cells
        for agent in cellmates: 
            if type(agent) == RoadAgent: 
                newPosition = self.getNextPosition(agent) # Get new a new position and save it as a tuple
                
                print("No car: ", self.noCarInFront(newPosition))
                print("Is green: ", self.isGreen(newPosition))
                print("Colission: ", self.continueIfColissionPoint(newPosition))
                
                if(self.noCarInFront(newPosition) or self.isGreen(newPosition)): # or self.continueIfColissionPoint(newPosition) 
                    self.model.grid.move_agent(self, newPosition)
                 
    def step(self) -> None:
        self.move() 


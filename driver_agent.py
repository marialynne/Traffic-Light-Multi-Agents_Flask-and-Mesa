'''
import mesa
from road_agent import RoadAgent
#from intersection_traffic_lights import IntersectionTrafficLightsAgent

class DriverAgent(mesa.Agent):
    def __init__(self, unique_id, model, layerLevel, velocity):
        super().__init__(unique_id, model)
        self.layerLevel = layerLevel
        self.velocity = velocity
        self.priority = 1
        
    # Funcion que determina que debe para cuando exista un coche adelante
    def stopIfReachedCar(self, agent):
        next_position = self.getNextPosition(agent)
        cellmates = self.model.grid.get_cell_list_contents([next_position])
        nextCellDrivers = 0
        for agent in cellmates: 
            print("agent ",type(agent))
            if type(agent) == DriverAgent:
                nextCellDrivers += 1
        #print("next cell drivers: ", nextCellDrivers)
        if nextCellDrivers >= 1:
            return False
        else:
            return True

    # Funcion que detiene el vehiculo cuando la siguiente casilla sea un semaforo y este en rojo
    def stopIfTrafickLightIsRed(self, agent):
        next_position = self.getNextPosition(agent)
        cellmates = self.model.grid.get_cell_list_contents([next_position])
        trafickLightStatus = True
        for agent in cellmates: 
            if type(agent) == SmartTrafficLightAgent or type(agent) == IntersectionTrafficLightsAgent:
                trafickLightStatus = False
        if not trafickLightStatus:
            return False
        else:
            return True
    
    # Funcion que detecte si el camino del frente es posible punto de colision, entonces, ya no se detiene si hay cochec al frente
    def continueIfColissionPoint(self, agent):
        next_position = self.getNextPosition(agent)
        if(next_position == [10, 9] or next_position == [9, 10] or next_position == [20, 9] or next_position == [19, 10]):
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
            if type(agent) == RoadAgent and (self.stopIfReachedCar(agent) or self.continueIfColissionPoint(agent)):
                new_position = self.getNextPosition(agent)
                self.model.grid.move_agent(self, new_position)
                 
    def step(self):
        self.move() 
        '''

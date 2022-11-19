import mesa
#from smart_traffic_light_agent import SmartTrafficLightAgent, RoadAgent
from road_agent import RoadAgent
#from intersection_traffic_lights import IntersectionTrafficLightsAgent

class DriverAgent(mesa.Agent):
    def __init__(self, unique_id, model, velocity, layerLevel = 1):
        super().__init__(unique_id, model)
        self.layerLevel = layerLevel
        self.velocity = velocity
        self.velocityIndex = 0
        self.priority = 1
        
    # Funcion que determina que debe para cuando exista un coche adelante
    def stopCar(self, agent):
        """ next_position = self.getNextPosition(agent)
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
        else:  """
        return True

    # Funcion que detiene el vehiculo cuando la siguiente casilla sea un semaforo y este en rojo
    
    # Funcion que detecte si el camino del frente es posible punto de colision, entonces, ya no se detiene si hay cochec al frente
    def continueIfColissionPoint(self, agent):
        next_position = self.getNextPosition(agent)
        return [next_position == [10, 10] or next_position == [10, 20] or next_position == [20, 10]]

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
        print("velocity: ", self.velocity, ", velocityIndex:", self.velocityIndex)
        if(self.velocityIndex <= self.velocity):
            self.velocityIndex += 1
        else:
            self.velocityIndex = 0
            self.move() 


import mesa
from road_agent import RoadAgent

class DriverAgent(mesa.Agent):
    def __init__(self, unique_id, model, layerLevel, velocity):
        super().__init__(unique_id, model)
        self.layerLevel = layerLevel
        self.velocity = velocity
        self.priority = 1
        
    # Funcion que determina que debe para cuando exista un coche adelante
    
    # Funcion que detiene el vehiculo cuando la siguiente casilla sea un semaforo y este en rojo
    
    # Funcion que detecte si el camino del frente es posible punto de colision, entonces, ya no se detiene si hay cochec al frente
    
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
            if type(agent) == RoadAgent:
                new_position = self.getNextPosition(agent);
                self.model.grid.move_agent(self, new_position)
                 
    def step(self):
        self.move();

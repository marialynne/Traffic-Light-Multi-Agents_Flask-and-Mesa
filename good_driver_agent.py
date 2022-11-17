import mesa
from road_agent import RoadAgent

class GoodDriverAgent(mesa.Agent):
    def __init__(self, unique_id, model, value, velocity):
        super().__init__(unique_id, model)
        self.value = value
        self.velocity = velocity
        self.priority = 1
        
    def getNextPosition(self, agent):
        if len(agent.directions) > 1:
            direction = self.random.choice(agent.directions) 
        if len(agent.directions) == 1:
            direction = agent.directions[0]
        x,y = self.pos
        if direction == "north":
            return(x,y+1)
        if direction == "south":
            return(x,y-1)
        if direction == "west":
            return(x-1,y)
        if direction == "east":
            return(x+1,y) 

    def move(self):
        cellmates = self.model.grid.get_cell_list_contents([self.pos])
        for agent in cellmates: 
            if type(agent) == RoadAgent:
                new_position = self.getNextPosition(agent);
                self.model.grid.move_agent(self, new_position)
                 
    def step(self):
        self.move();

import mesa
from good_driver_agent import GoodDriverAgent

class SmartTrafficLightAgent(mesa.Agent):

    def __init__(self, unique_id, model, value, direction, color):
        super().__init__(unique_id, model)
        self.color = color
        self.value = value
        self.direction = direction
        self.priority = 0
        self.queue = []
        self.id = unique_id

        
    def addCarToQueue (self, agent, ETA):
        self.queue.append((agent, ETA))
    
    def checkRoud(self):
        cell = 1
        x,y = self.pos
        while cell <= 8:
            if self.direction == "north":
                matesInCellPosition = self.model.grid.get_cell_list_contents((x,y-cell))
                print(matesInCellPosition)
                """ if len(matesInCellPosition) > 1: 
                    for agent in matesInCellPosition:
                        if type(agent) == GoodDriverAgent:
                            self.addCarToQueue(agent, agent.velocity * cell)  """
            cell+=1
                
    def step(self):
        self.checkRoud()
        print(self.queue)

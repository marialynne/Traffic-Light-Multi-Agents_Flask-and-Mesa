import mesa
import numpy as np
import random
from road_agent import RoadAgent
from smart_traffic_light_agent import SmartTrafficLightAgent
from good_driver_agent import GoodDriverAgent

class CityModel(mesa.Model):
        
    def __init__(self, agents, time):
        self.schedule= mesa.time.RandomActivationByType(self)
        self.running=True
        rows = 21
        columns = 21
        self.time = time
        self.grid= mesa.space.MultiGrid(rows, columns, False)
        id=0
        for row in range (rows):
            for col in range (columns):
                if row == 0 and (col <= 9 or 10 < col <= 19) or row == 10 and ( 1 <= col <= 9 or 10 < col <= 19):
                    id += self.addAgent(RoadAgent(id, self, ["north"], 0), row, col)  
                if row == 20 and  1 <= col <= 20:
                    id += self.addAgent(RoadAgent(id, self, ["south"], 0), row, col) 
                if col == 20 and (0 <= row <= 19) or col == 10 and ( 1 <= row <= 9 or 10 < row <= 19):
                    id += self.addAgent(RoadAgent(id, self, ["east"], 0), row, col) 
                if col == 0 and (1 <= row <= 9 or 10 < row <= 20):
                    id += self.addAgent(RoadAgent(id, self, ["west"], 0), row, col) 
                if (row == 0 and col == 10) or (row == 10 and col == 10):
                    id += self.addAgent(RoadAgent(id, self, ["north", "east"], 0), row, col) 
                if row == 10 and col == 0:
                    id += self.addAgent(RoadAgent(id, self, ["north", "west"], 0), row, col) 
                # Revisar colisiones despues
                if row == 0 and col == 0 and (col == 0 or col == 20) or row == 20 and (col == 0 or col == 20):
                    for i in range(round(agents/4)):
                        velocity = random.randrange(1, 4, 1)
                        id += self.addAgent(GoodDriverAgent(id, self, 1, velocity), row, col) 
                if col == 10 and (row == 9):
                        id += self.addAgent(SmartTrafficLightAgent(id, self, 2, "east", "yellow"), row, col) 
                if col == 10 and (row == 19):
                        id += self.addAgent(SmartTrafficLightAgent(id, self, 2, "east", "yellow"), row, col) 
                if row == 10 and (col == 9):
                        id += self.addAgent(SmartTrafficLightAgent(id, self, 2, "north", "yellow"), row, col) 
                if row == 10 and (col == 19):
                        id += self.addAgent(SmartTrafficLightAgent(id, self, 2, "north", "yellow"), row, col) 
                    
    def addAgent(self, agent, row, col):
        self.schedule.add(agent)
        self.grid.place_agent(agent,(row, col))
        return 1
                    
    def step(self):
        self.schedule.step()
        """ if CityModel.stopSimulation(self):
            self.running=False """
        self.time-=1

    # Modificar despues
    """ @staticmethod
    def stopSimulation(model):
        return [1 for agent in model.schedule.agents if type(agent) == RoombaAgent or model.time == 0]



         """
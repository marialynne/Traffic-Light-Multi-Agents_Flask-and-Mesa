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
                # Revisar colisiones despues y que se generen bien los agentes por cada casilla
                if row == 0 and col == 0 and (col == 0 or col == 20) or row == 20 and (col == 0 or col == 20):
                    for i in range(round(agents/4)):
                        velocity = random.randrange(1, 4, 1)
                        id += self.addAgent(GoodDriverAgent(id, self, 1, velocity), row, col) 
                        
                if (col == 10 and (row == 9 or row == 19)) or (col == 20 and row == 9):
                    id += self.addAgent(SmartTrafficLightAgent(id, self, 2, 8, "east", "yellow"), row, col) 
                if row == 10 and (col == 9 or col == 19):
                    id += self.addAgent(SmartTrafficLightAgent(id, self, 2, 8, "north", "yellow"), row, col) 
                if row == 20 and col == 11:
                    id += self.addAgent(SmartTrafficLightAgent(id, self, 2, 8, "south", "yellow"), row, col) 

    def addAgent(self, agent, row, col):
        self.schedule.add(agent)
        self.grid.place_agent(agent,(row, col))
        return 1
                    
    def step(self):
        self.schedule.step()
        CityModel.stopSimulation(self)

    # Modificar despues
    @staticmethod
    def stopSimulation(model):
        model.time-=1
        for agent in model.schedule.agents:
            if type(agent) == GoodDriverAgent or model.time == 0:
                model.running=False 

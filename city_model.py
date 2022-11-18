import mesa
import numpy as np
import random
from road_agent import RoadAgent
from smart_traffic_light_agent import SmartTrafficLightAgent
from intersection_traffic_lights import IntersectionTrafficLightsAgent
from driver_agent import DriverAgent

class CityModel(mesa.Model):     
    def __init__(self, agents, time):
        self.schedule = mesa.time.RandomActivationByType(self)
        self.running = True
        rows = 21
        columns = 21
        self.time = time
        self.steps = 0
        self.agents = agents
        self.grid = mesa.space.MultiGrid(rows, columns, False)
        self.id = 0
        for row in range (rows):
            for col in range (columns):
                if row == 0 and (col <= 9 or 10 < col <= 19) or row == 10 and ( 1 <= col <= 9 or 10 < col <= 19):
                    self.id += self.addAgent(RoadAgent(self.id, self, ["north"], 0), row, col)  
                if row == 20 and  1 <= col <= 20:
                    self.id += self.addAgent(RoadAgent(self.id, self, ["south"], 0), row, col) 
                if col == 20 and (0 <= row <= 19) or col == 10 and ( 1 <= row <= 9 or 10 < row <= 19):
                    self.id += self.addAgent(RoadAgent(self.id, self, ["east"], 0), row, col) 
                if col == 0 and (1 <= row <= 9 or 10 < row <= 20):
                    self.id += self.addAgent(RoadAgent(self.id, self, ["west"], 0), row, col) 
                if (row == 0 and col == 10) or (row == 10 and col == 10):
                    self.id += self.addAgent(RoadAgent(self.id, self, ["north", "east"], 0), row, col) 
                if row == 10 and col == 0:
                    self.id += self.addAgent(RoadAgent(self.id, self, ["north", "west"], 0), row, col) 

                # First intersection
                if (col == 10 and row == 9): 
                    smt1 = SmartTrafficLightAgent(self.id, self, 2, 8, "east")
                    self.id += self.addAgent(smt1, row, col) 
                if (col == 9 and row == 10): 
                    smt2 = SmartTrafficLightAgent(self.id, self, 2, 8, "north")
                    self.id += self.addAgent(smt2, row, col) 
                # Second intersection
                if (col == 20 and row == 9): 
                    smt3 = SmartTrafficLightAgent(self.id, self, 2, 8, "east")
                    self.id += self.addAgent(smt3, row, col) 
                if (col == 19 and row == 10): 
                    smt4 = SmartTrafficLightAgent(self.id, self, 2, 8, "north")
                    self.id += self.addAgent(smt4, row, col)
                # Third intersection
                if (col == 11 and row == 20): 
                    smt5 = SmartTrafficLightAgent(self.id, self, 2, 8, "south")
                    self.id += self.addAgent(smt5, row, col) 
                if (col == 10 and row == 19): 
                    smt6 = SmartTrafficLightAgent(self.id, self, 2, 8, "east")
                    self.id += self.addAgent(smt6, row, col) 

        self.id += self.addAgent(IntersectionTrafficLightsAgent(self.id, self, smt1, smt2), 10, 10)
        self.id += self.addAgent(IntersectionTrafficLightsAgent(self.id, self, smt3, smt4), 10, 20)
        self.id += self.addAgent(IntersectionTrafficLightsAgent(self.id, self, smt5, smt6), 20, 10)


    def addAgent(self, agent, row, col):
        self.schedule.add(agent)
        self.grid.place_agent(agent,(row, col))
        return 1

    def createDriver(self):
        corners = [(0, 0), (20, 0), (0, 20), (20, 20)]
        index = self.steps % 4
        velocity = random.randrange(1, 4, 1)
        #velocity = 1
        row, col = corners[index]
        self.id += self.addAgent(DriverAgent(self.id, self, 1, velocity), row, col)
                    
    def step(self):
        self.schedule.step()
        if self.steps < self.agents: self.createDriver()
        self.steps += 1
        #CityModel.stopSimulation(self)

    # Modificar despues
    """  @staticmethod
    def stopSimulation(model):
        model.time-=1
        for agent in model.schedule.agents:
            if type(agent) == GoodDriverAgent or model.time == 0:
                model.running=False  """

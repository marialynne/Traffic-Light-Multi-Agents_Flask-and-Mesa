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
                if row==0:
                    if  col==0:
                        p = RoadAgent(id,self,["north"],0)
                    if col==10:
                        p = RoadAgent(id,self,["west","north"],0)
                    else:
                        p = RoadAgent(id,self,["west"],0)
                    self.schedule.add(p)
                    self.grid.place_agent(p,(col,row))
                    id+=1  
                if col==0:
                    if row==20: 
                        p = RoadAgent(id,self,["east"],0)
                    else:    
                        p = RoadAgent(id,self,["north"],0)
                    self.schedule.add(p)
                    self.grid.place_agent(p,(col,row))
                    id+=1  
                if row==20:
                    p = RoadAgent(id,self,["east"],0)
                    self.schedule.add(p)
                    self.grid.place_agent(p,(col,row))
                    id+=1  
                if col==20:
                    p = RoadAgent(id,self,["south"],0)
                    self.schedule.add(p)
                    self.grid.place_agent(p,(col,row))
                    id+=1  
                if row==10: 
                    if col==0:
                        p = RoadAgent(id,self,["east","north"],0)
                    else:
                        p = RoadAgent(id,self,["east"],0)
                    self.schedule.add(p)
                    self.grid.place_agent(p,(col,row))
                    id+=1  
                if col==10:
                    p = RoadAgent(id,self,["north"],0)
                    self.schedule.add(p)
                    self.grid.place_agent(p,(col,row))
                    id+=1  

                
                if (col == 9 and row == 10) or (col == 10 and row == 9):
                    stl = SmartTrafficLightAgent(id,self,2)
                    self.schedule.add(stl)
                    self.grid.place_agent(stl,(col,row))
                    id+=1  
                if row==0 and col==0:
                    agent = GoodDriverAgent(id,self,1)
                    self.schedule.add(agent)
                    self.grid.place_agent(agent,(col,row))
                    id+=1  

                """ if (col == 0 and col == 10) or (col == 1 and col == 11) or (col == 9 and col == 20) or (col == 10 and col == 19):
                    tl = TrafficLightAgent(id,self)
                    self.schedule.add(tl)
                    self.grid.place_agent(tl,(col,row))
                    id+=1 """
                """ if (col == 0 and col==0) or (col == 0 and col==20) or (col == 20 and col==0) or (col == 20 and col==20):
                    type = random.randit(0,4)
                    for agent in range (agents/4):
                        if type == 0:
                            agent = AmbulanceAgent(id,self)
                        if type == 1:
                            agent = CrazyDriverAgent(id,self)
                        if type == 2:
                            agent = GoodDriverAgent(id,self)
                        if type == 3:
                            agent = TruckAgent(id,self)
                        if type == 4:
                            agent = WannabeCrazyDriverAgent(id,self)
                        self.schedule.add(agent)
                        self.grid.place_agent(agent,(col,row))
                        id+=1 """
    
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
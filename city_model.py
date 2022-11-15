import mesa
import numpy as np
import random

class CityModel(mesa.Model):
    
    def __init__(self,agents,time):
        self.schedule= mesa.time.RandomActivationByType(self)
        self.running=True
        rows = 21
        columns = 21
        self.time = time
        self.grid= mesa.space.MultiGrid(rows, columns, False)
        id=0
        for row in range (rows):
            for col in range (columns):
                if row == 0 or col==0 or row==20 or col==20 or row==10 or col==10:
                    p = RoadAgent(id,self)
                    self.schedule.add(p)
                    self.grid.place_agent(p,(row,col))
                    id+=1
                if (row == 10 and col == 10) or (row == 11 and col == 11):
                    stl = SmartTrafficLightAgent(id,self)
                    self.schedule.add(stl)
                    self.grid.place_agent(stl,(row,col))
                    id+=1
                if (row == 0 and col == 10) or (row == 1 and col == 11) or (row == 9 and col == 20) or (row == 10 and col == 19):
                    tl = TrafficLightAgent(id,self)
                    self.schedule.add(tl)
                    self.grid.place_agent(tl,(row,col))
                    id+=1
                if (row == 0 and col==0) or (row == 0 and col==20) or (row == 20 and col==0) or (row == 20 and col==20):
                    type = random.randit(0,4)
                    for agent in range (agents/4):
                        if type == 0:
                            ambulance = AmbulanceAgent(id,self)
                            self.schedule.add(ambulance)
                            self.grid.place_agent(ambulance,(row,col))
                            id+=1
                        if type == 1:
                            crazyDriver = CrazyDriverAgent(id,self)
                            self.schedule.add(crazyDriver)
                            self.grid.place_agent(crazyDriver,(row,col))
                            id+=1
                        if type == 2:
                            goodDriver = GoodDriverAgent(id,self)
                            self.schedule.add(goodDriver)
                            self.grid.place_agent(goodDriver,(row,col))
                            id+=1
                        if type == 3:
                            truck = TruckAgent(id,self)
                            self.schedule.add(truck)
                            self.grid.place_agent(truck,(row,col))
                            id+=1
                        if type == 4:
                            wannabeCrazyDriver = WannabeCrazyDriverAgent(id,self)
                            self.schedule.add(wannabeCrazyDriver)
                            self.grid.place_agent(wannabeCrazyDriver,(row,col))
                            id+=1

    
    def step(self):
        self.schedule.step()
        if CityModel.stopSimulation(self):
            self.running=False
        self.time-=1

    
    @staticmethod
    def stopSimulation(model):
        return [1 for agent in model.schedule.agents if type(agent) == RoombaAgent or model.time == 0]



        
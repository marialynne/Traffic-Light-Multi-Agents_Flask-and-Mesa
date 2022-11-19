import mesa
import random
#from driver_agent import DriverAgent
from smart_traffic_light_agent import SmartTrafficLightAgent, DriverAgent

class IntersectionTrafficLightsAgent(mesa.Agent):
    def __init__(self, unique_id, model, smt1, smt2, layerLevel = 0):
        super().__init__(unique_id, model)
        self.smt1 = smt1
        self.smt2 = smt2
        self.layerLevel = layerLevel
        
    def chechPriorities(self):
        agentsInCell = self.model.grid.get_cell_list_contents([self.pos])
        if not DriverAgent in agentsInCell:
            if self.smt1.priority < self.smt2.priority:
                self.smt1.changeStatus("green")
                self.smt2.changeStatus("red")
            elif self.smt1.priority > self.smt2.priority:
                self.smt2.changeStatus("green")
                self.smt1.changeStatus("red")
            elif self.smt1.priority == self.smt2.priority and (not self.smt1.queue and not self.smt2.queue):
                randomLight = random.randrange(1, 2, 1)
                if randomLight == 1: 
                    self.smt2.changeStatus("green")
                    self.smt1.changeStatus("red")
                elif randomLight == 2:
                    self.smt1.changeStatus("green")
                    self.smt2.changeStatus("red")
        
    def step(self):
        self.chechPriorities()

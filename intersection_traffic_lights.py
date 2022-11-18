import mesa
import random
from smart_traffic_light_agent import SmartTrafficLightAgent

class IntersectionTrafficLightsAgent(mesa.Agent):
    def __init__(self, unique_id, model, smt1, smt2, layerLevel = 0):
        super().__init__(unique_id, model)
        self.smt1 = smt1
        self.smt2 = smt2
        self.layerLevel = layerLevel
        
    def chechPriorities(self):
        if self.smt1.priority > self.smt2priority:
            self.smt1.color = "green"
            self.smt2.color = "red"
        else:
            self.smt2.color = "green"
            self.smt1.color = "red"
        
    def step(self):
        self.chechPriorities()

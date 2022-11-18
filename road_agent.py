import mesa

class RoadAgent(mesa.Agent):

    def __init__(self, unique_id, model, directions, layerLevel):
        super().__init__(unique_id, model)
        self.directions = directions
        self.layerLevel = layerLevel

    def step(self):
        return

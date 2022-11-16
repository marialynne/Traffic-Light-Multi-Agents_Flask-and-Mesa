import mesa

class RoadAgent(mesa.Agent):

    def __init__(self, unique_id, model, directions, value):
        super().__init__(unique_id, model)
        self.directions = directions
        self.value = value

    def step(self):
        return

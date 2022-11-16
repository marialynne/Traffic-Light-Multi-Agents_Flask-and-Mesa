import mesa

class SmartTrafficLightAgent(mesa.Agent):

    def __init__(self, unique_id, model, value):
        super().__init__(unique_id, model)
        self.color = "red"
        self.value = value

    def step(self):
        return

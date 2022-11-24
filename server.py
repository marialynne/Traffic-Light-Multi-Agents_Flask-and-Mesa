from city_model import CityModel
import mesa
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from mesa.visualization.UserParam import UserSettableParameter
from mesa.visualization.modules import ChartModule, CanvasGrid

PIXELS_GRID = 600

def agent_portrayal(agent): # A color is assigned to each type of agent
    portrayal = {"Shape": "circle", "Filled": "true"}
    if agent.layerLevel == 2: # Traffic Lights
        portrayal["Shape"] = "arrowHead"
        portrayal["Layer"] = 2
        portrayal["scale"] = 0.8
        portrayal["Color"] = agent.color
        if agent.direction == "east":
            portrayal["heading_x"] = 1
            portrayal["heading_y"] = 0
        elif agent.direction == "north":
            portrayal["heading_x"] = 0
            portrayal["heading_y"] = 1
        elif agent.direction == "south":
            portrayal["heading_x"] = 0
            portrayal["heading_y"] = -1
        elif agent.direction == "west":
            portrayal["heading_x"] = -1
            portrayal["heading_y"] = 0
    elif agent.layerLevel == 1: # Cars
        portrayal["Color"] = "blue"
        portrayal["Layer"] = 1
        portrayal["r"] = 0.8
    elif agent.layerLevel == 4:
        portrayal["Shape"] = "rect"
        portrayal["Color"] = "gray"
        portrayal["Layer"] = 0
        portrayal["h"] = 1
        portrayal["w"] = 1
    else: # Road
        portrayal["Shape"] = "rect"
        portrayal["Color"] = "black"
        portrayal["Layer"] = 0
        portrayal["h"] = 1
        portrayal["w"] = 1
    return portrayal

params = {
    "agents": 15,
    "time": 25
}
results = mesa.batch_run(
    CityModel,
    parameters=params,
    iterations=1,
    max_steps=500,  # time
    number_processes=1,
    data_collection_period=1,
    display_progress=True,
)

results_df = pd.DataFrame(results)

print(results_df)

congestion = pd.DataFrame(results_df, columns=['Congestion'])
crashes = pd.DataFrame(results_df, columns=['Crashes'])
sanity = pd.DataFrame(results_df, columns=['Sanity'])
movesByDriver = pd.DataFrame(results_df, columns=['MovesByDriver'])

""" congestion_filtered = congestion[(results_df.Step == 10)]
crashes_filtered = crashes[(results_df.Step == 10)]
sanity_filtered = sanity[(results_df.Step == 10)]
movesByDriver_filtered = movesByDriver[(results_df.Step == 10)] """

""" congestion.plot()
crashes.plot()
sanity.plot()
movesByDriver.plot()
# save the model data (stored in the pandas gini object) to CSV
results_df.to_csv("model_data.csv")
plt.show() """
  
simulation_params = {
    "agents": UserSettableParameter(
        "slider",
        "Number of Agents",
        value=4,
        min_value=1,
        max_value=30,
        step=1,
        description="Number of Agents",
    ),
    "time": UserSettableParameter(
        "number",
        "Time",
        25,
        description="Time to end",
    )
}

chartCrashes = ChartModule([{"Label": "Crashes", "Color": "Red"}], data_collector_name='datacollector')
chartCongestion = ChartModule([{"Label": "Congestion", "Color": "Red"}], data_collector_name='datacollector')
chartSanity = ChartModule([{"Label": "Sanity", "Color": "Red"}], data_collector_name='datacollector')
#chartTimeOfTrafficLightOn = ChartModule([{"Label": "TimeOfTrafficLightOn", "Color": "Blue"}], data_collector_name='datacollector')
#chartSuccessRateWithoutCrash = ChartModule([{"Label": "SuccessRateWithoutCrash", "Color": "Blue"}], data_collector_name='datacollector')
chartMovesByDriver = ChartModule([{"Label": "MovesByDriver", "Color": "Blue"}], data_collector_name='datacollector')

grid = CanvasGrid(agent_portrayal, 21, 21, PIXELS_GRID, PIXELS_GRID)

server = mesa.visualization.ModularServer(
    CityModel, [grid,
                chartCrashes,
                chartSanity,
                chartCongestion,
                #chartTimeOfTrafficLightOn,
                #chartSuccessRateWithoutCrash,
                chartMovesByDriver], 
    "Smart Traffic Light", simulation_params
)

server.port = 8525
server.launch()

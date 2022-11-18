from city_model import *
import matplotlib.pyplot as plt
import pandas as pd
from mesa.visualization.UserParam import UserSettableParameter

PIXELS_GRID = 500

""" 
params = {
    "agents": 1,
    "rows": 10,
    "columns": 10,
    "x_start": 0,
    "y_start": 0,
    "percentage_dirty_cells": 45,
    "moves": 25
}
results = mesa.batch_run(
    RoomModel,
    parameters=params,
    iterations=5,
    max_steps=100,  # time
    number_processes=1,
    data_collection_period=1,
    display_progress=True,
) """

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
    else: # Road
        portrayal["Shape"] = "rect"
        portrayal["Color"] = "black"
        portrayal["Layer"] = 0
        portrayal["h"] = 1
        portrayal["w"] = 1
    return portrayal

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


""" def get_clean_percentage(model):
    return f"Percentage of clean cells: {model.clean_percentage:.2f} %"


def get_current_move(model):
    return f"Time to finish: {model.timeToEnd}"

 """
grid = mesa.visualization.CanvasGrid(
    agent_portrayal, 21, 21, 600, 600)

server = mesa.visualization.ModularServer(
    CityModel, [
        grid], "Smart Traffic Light", simulation_params
)

server.port = 8522
server.launch()

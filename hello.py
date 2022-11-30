from flask import Flask, request, make_response
import mesa
from city_model import CityModel
import pandas as pd
import json
import os

app = Flask(__name__, static_url_path='')
port = int(os.getenv('PORT', 8000))

class DataStore():
    simulation = CityModel(20)

data = DataStore()

@app.route("/")
def run_simulation():
    agents = request.args.get('agents')
    if not agents:
        maybeJson = data.simulation.step()
        return json.dumps(maybeJson)
    else:
        data.simulation = CityModel(int(agents))
        return "Created simulation"

@app.route("/batch")
def batchRoute():
    return "aqui va forma"

@app.route("/run-batch")
def runBatch():
    agents = request.args.get('agents')
    iteration = request.args.get('iteration')
    maxSteps = request.args.get('steps')

    if agents and iteration and maxSteps:
        results = mesa.batch_run(
            CityModel,
            parameters={ "agents": int(agents) },
            iterations=int(iteration),
            max_steps=int(maxSteps),  # time
            number_processes=1,
            data_collection_period=-1,
            display_progress=True,
        )
        results_df = pd.DataFrame(results)
        # dataResults = results_df.to_csv("model_data.csv")
        resp = make_response(results_df.to_csv())
        resp.headers["Content-Disposition"] = "attachment; filename=data.csv"
        resp.headers["Content-Type"] = "text/csv"
        return resp
    else:
        return "DATOS INCORRECTOS"


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port, debug=True)

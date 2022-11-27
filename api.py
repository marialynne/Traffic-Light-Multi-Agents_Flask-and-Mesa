from flask import Flask, request
from city_model import CityModel
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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port, debug=True)

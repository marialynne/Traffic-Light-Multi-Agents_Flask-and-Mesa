from flask import Flask, session, request
from city_model import CityModel
import mesa
import json, logging, os, atexit

app = Flask(__name__, static_url_path='')
port = int(os.getenv('PORT', 8000))

class DataStore():
    simulation = CityModel(5, 100)

data = DataStore()

@app.route("/")
def run_simulation():
    agents = request.args.get('agents')
    time = request.args.get('time')
    if not agents and not time:
        maybeJson = data.simulation.step()
        return json.dumps(maybeJson)
    else:
        data.simulation = CityModel(int(agents), int(time))
        return "Created simulation"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port, debug=True)
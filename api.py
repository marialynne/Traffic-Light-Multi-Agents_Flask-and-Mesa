from flask import Flask
from city_model import CityModel
import mesa
import json, logging, os, atexit

app = Flask(__name__, static_url_path='')
port = int(os.getenv('PORT', 8000))
simulation = CityModel(5, 100)


@app.route("/")
def run_simulation():
    maybeJson = simulation.step()
    return json.dumps(maybeJson)
    
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port, debug=True)
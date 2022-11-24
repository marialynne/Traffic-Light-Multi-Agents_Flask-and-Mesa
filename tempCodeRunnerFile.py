not agents and not time:
        maybeJson = data.simulation.step()
        return json.dumps(maybeJson)
    else:
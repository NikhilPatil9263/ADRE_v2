def apply_event(event, twin):
    etype = event["type"]
    data = event["data"]

    if etype == "traffic":
        for route_id, multiplier in data.items():
            twin.routes[route_id].traffic_multiplier = multiplier
            twin.routes[route_id].recompute()

    elif etype == "weather":
        for route_id, multiplier in data.items():
            twin.routes[route_id].weather_multiplier = multiplier
            twin.routes[route_id].recompute()

    elif etype == "fuel":
        for vehicle in twin.vehicles.values():
            vehicle.fuel_price = data["diesel_price"]

    twin.update_timestamp()

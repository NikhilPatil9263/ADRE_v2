def predict_fuel_liters(distance_km, mileage_kmpl):
    return distance_km / mileage_kmpl


def estimate_fuel_cost(fuel_liters, diesel_price):
    return fuel_liters * diesel_price

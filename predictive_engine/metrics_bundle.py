from predictive_engine.eta_predictor import predict_eta
from predictive_engine.fuel_predictor import (
    predict_fuel_liters,
    estimate_fuel_cost
)
from predictive_engine.carbon_predictor import predict_carbon


def compute_metrics(route, vehicle):
    """
    Computes all predictive metrics for a route.
    Traffic & weather are already baked into effective_distance.
    """

    # ================= ETA =================
    eta = predict_eta(route.effective_distance)

    # ================= FUEL =================
    fuel_liters = predict_fuel_liters(
        route.effective_distance,
        vehicle.mileage_kmpl
    )

    fuel_cost = round(
        estimate_fuel_cost(fuel_liters, vehicle.fuel_price),
        2
    )

    # ================= CARBON =================
    co2 = predict_carbon(fuel_liters)

    return {
        "route_id": route.route_id,
        "eta_min": round(eta, 2),
        "fuel_liters": round(fuel_liters, 2),
        "fuel_cost": fuel_cost,
        "co2_kg": round(co2, 2)
    }

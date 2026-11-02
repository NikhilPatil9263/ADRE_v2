from predictive_engine.metrics_bundle import compute_metrics
from digital_twin.twin_state import TwinState

def run_predictions(twin: TwinState):
    predictions = []

    for route in twin.routes.values():
        for vehicle in twin.vehicles.values():
            metrics = compute_metrics(route, vehicle)
            predictions.append(metrics)

    return predictions

# run_phase3.py

from digital_twin.twin_state import TwinState
from digital_twin.route_model import Route
from digital_twin.vehicle_model import Vehicle
from digital_twin.loss_engine import LossEngine

from decision_engine.route_optimizer import RouteOptimizer
from explainability.explanation_engine import ExplanationEngine
from explainability.llm_reasoner import LLMReasoner

from services.map_services import MapService
from services.traffic_service import TrafficService
from services.weather_service import WeatherService
from services.city_registry import CITY_COORDS


# ================= ETA ADJUSTMENT (TRAFFIC + WEATHER) =================

def apply_conditions_to_eta(base_eta_min, traffic_multiplier, weather_context):
    """
    ETA = base ETA × traffic × weather
    """

    eta_after_traffic = base_eta_min * traffic_multiplier

    if not weather_context or "condition" not in weather_context:
        condition = "unknown"
        weather_multiplier = 1.0
    else:
        condition = weather_context["condition"]

        if condition in ["rain", "storm", "snow"]:
            weather_multiplier = 1.20
        elif condition in ["fog", "mist", "clouds"]:
            weather_multiplier = 1.10
        else:
            weather_multiplier = 1.00

    final_eta = round(eta_after_traffic * weather_multiplier, 2)

    print(
        f"⏱️ ETA ADJUSTMENT | "
        f"Traffic x{traffic_multiplier} | "
        f"Weather: {condition} | "
        f"Base: {base_eta_min:.2f} → Final: {final_eta:.2f}"
    )

    return final_eta


# ================= PREDICTION OUTPUT =================

def pretty_print(results):
    print("\n=== PREDICTIVE ENGINE OUTPUT ===\n")

    for r in results:
        print(f"Route: {r['route_id']}")
        print(f"  ETA        : {round(r['eta_min'], 2)} minutes")
        print(f"  Fuel       : {round(r['fuel_liters'], 2)} liters")
        print(f"  Fuel Cost  : ₹{round(r['fuel_cost'], 2)}")
        print(f"  CO₂        : {round(r['co2_kg'], 2)} kg")
        print("-" * 40)


# ================= MAIN EXECUTION =================

if __name__ == "__main__":

    # ================= PHASE 1–2: DIGITAL TWIN =================

    twin = TwinState()
    map_service = MapService()
    traffic_service = TrafficService()
    weather_service = WeatherService()

    print("Routes in twin (before):", twin.routes)

    # ================= WEATHER OVERRIDE (PHASE D TESTING) =================

    # Uncomment ONE line at a time for validation

    FORCE_WEATHER = {
        # "Chennai-Mumbai": "storm",
        # "Chennai-Bengaluru": "storm"
    }

    # ================= ROUTES =================

    route_pairs = [
        ("Chennai", "Mumbai"),
        ("Chennai", "Bengaluru")
    ]

    for origin_city, dest_city in route_pairs:

        origin_coords = CITY_COORDS[origin_city]
        destination_coords = CITY_COORDS[dest_city]

        route_id = f"{origin_city}-{dest_city}"

        print(f"\n📍 Computing real route distance: {route_id}")

        try:
            distance_km = map_service.get_route_distance_km(
                origin_coords, destination_coords
            )

            print(f"   → Distance: {distance_km} km")

        except Exception:
            from geopy.distance import geodesic

            print("⚠️ Route API failed — using geodesic fallback")

            distance_km = round(
                geodesic(origin_coords, destination_coords).km, 2
            )

        route = Route(
            route_id=route_id,
            origin=origin_city,
            destination=dest_city,
            distance_km=distance_km
        )

        # ================= MIDPOINT =================

        mid_lat = (origin_coords[0] + destination_coords[0]) / 2
        mid_lon = (origin_coords[1] + destination_coords[1]) / 2

        # ================= TRAFFIC =================

        try:
            traffic_multiplier = traffic_service.get_traffic_multiplier(
                mid_lat, mid_lon
            )

        except Exception:
            print("⚠️ Traffic API failed — using fallback")
            traffic_multiplier = 1.0

        route.traffic_multiplier = traffic_multiplier

        # ================= WEATHER =================

        try:
            weather_context = weather_service.get_weather_context(
                mid_lat, mid_lon
            )

            print(
                f"🌦️ WEATHER API CHECK [{route_id}] -> {weather_context}"
            )

        except Exception:
            print("⚠️ Weather API failed — using fallback")
            weather_context = {"condition": "clear"}

        # ---------- WEATHER OVERRIDE ----------

        if route_id in FORCE_WEATHER:

            forced_condition = FORCE_WEATHER[route_id]

            print(
                f"🧪 WEATHER OVERRIDE APPLIED "
                f"[{route_id}] -> {forced_condition}"
            )

            weather_context["condition"] = forced_condition

        route.weather_context = weather_context

        route.weather_multiplier = weather_service.get_weather_multiplier(
            weather_context
        )

        # ================= EFFECTIVE DISTANCE =================

        route.effective_distance = round(
            distance_km
            * route.traffic_multiplier
            * route.weather_multiplier,
            2
        )

        twin.routes[route_id] = route

    # ================= VEHICLE =================

    vehicle = Vehicle(
        vehicle_id="TRUCK-01",
        mileage_kmpl=12
    )

    vehicle.fuel_price = 90.0

    twin.vehicles[vehicle.vehicle_id] = vehicle

    print("\nRoutes in twin (after):", twin.routes)

    # ================= PHASE 3: PREDICTION =================

    predictions = []

    for route_id, route in twin.routes.items():

        base_eta = route.distance_km  # 1 km ≈ 1 min

        eta_min = apply_conditions_to_eta(
            base_eta,
            route.traffic_multiplier,
            route.weather_context
        )

        fuel_used = route.effective_distance / vehicle.mileage_kmpl
        fuel_cost = fuel_used * vehicle.fuel_price
        co2_kg = fuel_used * 2.68

        predictions.append({
            "route_id": route_id,
            "eta_min": eta_min,
            "fuel_liters": fuel_used,
            "fuel_cost": fuel_cost,
            "co2_kg": co2_kg
        })

    pretty_print(predictions)

    # ================= PHASE 4: LOSS =================

    loss_engine = LossEngine()
    enriched_results = []

    print("\n=== LOSS ESTIMATION OUTPUT ===\n")

    for r in predictions:

        route = twin.routes[r["route_id"]]

        losses = loss_engine.compute_losses(
            eta_min=r["eta_min"],
            base_eta_min=route.distance_km,
            fuel_used=r["fuel_liters"],
            base_fuel=route.distance_km / vehicle.mileage_kmpl,
            fuel_price=vehicle.fuel_price,
            co2_kg=r["co2_kg"],
            weather_context=route.weather_context
        )

        print(f"Route: {r['route_id']}")

        for k, v in losses.items():
            print(
                f"  {k.replace('_', ' ').title():15}: "
                f"₹{round(v, 2)}"
            )

        print("-" * 40)

        enriched_results.append({
            "route_id": r["route_id"],
            "eta_min": r["eta_min"],
            "fuel_cost": r["fuel_cost"],
            "co2_kg": r["co2_kg"],
            "total_loss": losses["total_loss"]
        })

    # ================= PHASE 5: OPTIMIZATION =================

    optimizer = RouteOptimizer()

    best_route = optimizer.select_best_route(enriched_results)

    print("\n=== ROUTE OPTIMIZATION DECISION ===\n")

    print(f"✅ Best Route Selected : {best_route['route_id']}")
    print(
        f"💰 Minimum Total Loss  : "
        f"₹{round(best_route['total_loss'], 2)}"
    )

    # ================= PHASE 6: EXPLANATION =================

    explain_engine = ExplanationEngine()

    rejected_routes = [
        r for r in enriched_results
        if r["route_id"] != best_route["route_id"]
    ]

    print("\n=== AI EXPLANATION ===\n")

    print(
        explain_engine.explain_route_decision(
            best_route,
            rejected_routes
        )
    )

    # ================= PHASE 6B: LLM =================

    llm_reasoner = LLMReasoner()

    llm_output = llm_reasoner.generate_reasoning(
        best_route,
        enriched_results
    )

    print("\n=== LLM REASONING (PHASE 6B) ===\n")

    print(llm_output["llm_reasoning"])


# ================= DASHBOARD EXECUTION =================

def run_adre_for_dashboard():
    """
    Runs Phase 3–6 and returns structured results for Streamlit.
    """

    results = {
        "routes": [],
        "best_route": None,
        "explanation": None,
        "llm_reasoning": None,
        "prompt_used": None
    }

    # ================= INITIALIZATION =================

    twin = TwinState()

    map_service = MapService()
    traffic_service = TrafficService()
    weather_service = WeatherService()

    route_pairs = [
        ("Chennai", "Mumbai"),
        ("Chennai", "Bengaluru")
    ]

    vehicle = Vehicle(
        vehicle_id="TRUCK-01",
        mileage_kmpl=12
    )

    vehicle.fuel_price = 90.0

    # ================= ROUTE PROCESSING =================

    for origin_city, dest_city in route_pairs:

        origin_coords = CITY_COORDS[origin_city]
        destination_coords = CITY_COORDS[dest_city]

        route_id = f"{origin_city}-{dest_city}"

        distance_km = map_service.get_route_distance_km(
            origin_coords,
            destination_coords
        )

        mid_lat = (origin_coords[0] + destination_coords[0]) / 2
        mid_lon = (origin_coords[1] + destination_coords[1]) / 2

        traffic_multiplier = traffic_service.get_traffic_multiplier(
            mid_lat,
            mid_lon
        )

        weather_context = weather_service.get_weather_context(
            mid_lat,
            mid_lon
        )

        weather_multiplier = weather_service.get_weather_multiplier(
            weather_context
        )

        # ================= ETA PREDICTION =================

        base_eta = distance_km

        eta_min = apply_conditions_to_eta(
            base_eta,
            traffic_multiplier,
            weather_context
        )

        # ================= FUEL AND EMISSIONS =================

        effective_distance = (
            distance_km
            * traffic_multiplier
            * weather_multiplier
        )

        fuel_used = effective_distance / vehicle.mileage_kmpl

        fuel_cost = fuel_used * vehicle.fuel_price

        co2_kg = fuel_used * 2.68

        # ================= LOSS ESTIMATION =================

        loss_engine = LossEngine()

        losses = loss_engine.compute_losses(
            eta_min=eta_min,
            base_eta_min=distance_km,
            fuel_used=fuel_used,
            base_fuel=distance_km / vehicle.mileage_kmpl,
            fuel_price=vehicle.fuel_price,
            co2_kg=co2_kg,
            weather_context=weather_context
        )

        # ================= STORE ROUTE RESULTS =================

        route = Route(
            route_id=route_id,
            origin=origin_city,
            destination=dest_city,
            distance_km=distance_km
        )

        route.traffic_multiplier = traffic_multiplier
        route.weather_context = weather_context
        route.weather_multiplier = weather_multiplier
        route.effective_distance = effective_distance

        twin.routes[route_id] = route

        results["routes"].append({
            "route_id": route_id,
            "eta_min": round(eta_min, 2),
            "fuel_cost": round(fuel_cost, 2),
            "co2_kg": round(co2_kg, 2),
            "total_loss": round(losses["total_loss"], 2)
        })

    # ================= PHASE 5: OPTIMIZATION =================

    optimizer = RouteOptimizer()

    best = optimizer.select_best_route(
        results["routes"]
    )

    # ================= PHASE 6: EXPLANATION =================

    explain_engine = ExplanationEngine()

    rejected_routes = [
        r for r in results["routes"]
        if r["route_id"] != best["route_id"]
    ]

    explanation = explain_engine.explain_route_decision(
        best,
        rejected_routes
    )

    # ================= PHASE 6B: LLM REASONING =================

    llm_reasoner = LLMReasoner()

    llm_output = llm_reasoner.generate_reasoning(
        best,
        results["routes"]
    )

    # ================= FINAL RESULTS =================

    results["best_route"] = best
    results["explanation"] = explanation
    results["llm_reasoning"] = llm_output["llm_reasoning"]
    results["prompt_used"] = llm_output["prompt_used"]

    return results
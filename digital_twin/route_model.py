# digital_twin/route_model.py

class Route:
    def __init__(self, route_id, origin, destination, distance_km):
        self.route_id = route_id
        self.origin = origin
        self.destination = destination

        # Core geometry
        self.distance_km = distance_km
        self.effective_distance = distance_km

        # --- Traffic & Weather Context (Phase 8A + 8B) ---
        self.traffic_multiplier = 1.0
        self.weather_multiplier = 1.0

        self.traffic_delay_min = 0
        self.weather_delay_min = 0

        self.weather_condition = "clear"
        self.weather_context = None  # ← Phase 8B (API driven)

        # Filled by engines
        self.eta_min = None
        self.fuel_liters = None
        self.fuel_cost = None
        self.co2_kg = None
        self.risk_score = None

        # Apply deterministic models
        self.apply_traffic_conditions()
        self.apply_weather_conditions()

    # -------------------------------------------------
    # Phase 8A: Deterministic Traffic Model
    # -------------------------------------------------
    def apply_traffic_conditions(self):
        if self.distance_km > 800:
            self.traffic_multiplier = 1.30
            self.traffic_delay_min = 45

        elif self.distance_km > 300:
            self.traffic_multiplier = 1.15
            self.traffic_delay_min = 20

        else:
            self.traffic_multiplier = 1.05
            self.traffic_delay_min = 10

    # -------------------------------------------------
    # Phase 8A: Weather placeholder (overridden by API)
    # -------------------------------------------------
    def apply_weather_conditions(self):
        if self.weather_condition == "rain":
            self.weather_multiplier = 1.10
            self.weather_delay_min = 15

        elif self.weather_condition == "storm":
            self.weather_multiplier = 1.25
            self.weather_delay_min = 40

        else:
            self.weather_multiplier = 1.00
            self.weather_delay_min = 0

    # -------------------------------------------------
    # Phase 8B: Effective Distance
    # -------------------------------------------------
    def update_effective_distance(self):
        self.effective_distance = round(
            self.distance_km
            * self.traffic_multiplier
            * self.weather_multiplier,
            2
        )

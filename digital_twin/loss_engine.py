# digital_twin/loss_engine.py

class LossEngine:
    def __init__(self):
        # Cost constants (₹)
        self.delay_cost_per_min = 5.0        # cost of delay per minute
        self.co2_cost_per_kg = 2.0           # carbon cost per kg CO2

        # Weather penalty mapping
        self.weather_penalties = {
            "rain": 1.10,
            "storm": 1.25,
            "snow": 1.30,
            "fog": 1.15,
            "mist": 1.12,
            "clouds": 1.05,
            "clear": 1.0
        }

    def compute_losses(
        self,
        eta_min,
        base_eta_min,
        fuel_used,
        base_fuel,
        fuel_price,
        co2_kg,
        weather_context=None
    ):
        """
        Computes total loss including:
        - Delay loss
        - Fuel loss
        - Emission loss
        - Weather risk penalty
        """

        # ---------------- DELAY LOSS ----------------
        delay_minutes = max(0, eta_min - base_eta_min)
        delay_loss = delay_minutes * self.delay_cost_per_min

        # ---------------- FUEL LOSS ----------------
        extra_fuel = max(0, fuel_used - base_fuel)
        fuel_loss = extra_fuel * fuel_price

        # ---------------- EMISSION LOSS ----------------
        emission_loss = co2_kg * self.co2_cost_per_kg

        # ---------------- WEATHER LOSS ----------------
        weather_loss = 0.0
        weather_multiplier = 1.0

        if weather_context:
            condition = weather_context.get("condition", "clear")
            weather_multiplier = self.weather_penalties.get(condition, 1.0)

            # Weather loss is applied on delay + fuel impact
            weather_loss = (delay_loss + fuel_loss) * (weather_multiplier - 1)

        # ---------------- TOTAL LOSS ----------------
        total_loss = (
            delay_loss +
            fuel_loss +
            emission_loss +
            weather_loss
        )

        return {
            "delay_loss": delay_loss,
            "fuel_loss": fuel_loss,
            "emission_loss": emission_loss,
            "weather_loss": weather_loss,
            "total_loss": total_loss
        }

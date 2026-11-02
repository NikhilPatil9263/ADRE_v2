class ExplanationEngine:

    def explain_route_decision(self, best_route, rejected_routes):
        """
        Generates a human-readable explanation for why a route was selected.
        """

        explanation = (
            f"Route {best_route['route_id']} was selected as the optimal route. "
            f"It resulted in the lowest total estimated loss of ₹{best_route['total_loss']}. "
        )

        if rejected_routes:
            explanation += "Other routes were rejected due to higher total loss caused by "

            reasons = []
            for route in rejected_routes:
                reasons.append(
                    f"higher fuel usage, carbon impact, or delays on route {route['route_id']}"
                )

            explanation += "; ".join(reasons) + "."

        explanation += (
            " The decision balances delivery time, fuel efficiency, and environmental impact "
            "to minimize overall operational cost."
        )

        return explanation
    def apply_weather_to_eta(self, base_eta_min, weather_context):
        if not weather_context:
            return base_eta_min

        condition = weather_context.get("condition", "clear")

        if condition in ["rain", "storm", "snow"]:
            multiplier = 1.2
        elif condition in ["fog", "mist"]:
            multiplier = 1.15
        else:
            multiplier = 1.0

        return base_eta_min * multiplier

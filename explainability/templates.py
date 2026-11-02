def route_explanation_template(best_route, candidate_routes):
    explanation = []
    explanation.append(
        f"Route {best_route['route_id']} was selected as the optimal route."
    )

    explanation.append(
        f"It resulted in the lowest total estimated loss of ₹{best_route['total_loss']}."
    )

    for r in candidate_routes:
        if r["route_id"] != best_route["route_id"]:
            explanation.append(
                f"Route {r['route_id']} was rejected due to higher total loss "
                f"(₹{r['total_loss']}) caused by delays, fuel usage, carbon impact, or SLA penalties."
            )

    explanation.append(
        "The decision balances delivery speed, fuel efficiency, environmental impact, "
        "and operational risk."
    )

    return " ".join(explanation)

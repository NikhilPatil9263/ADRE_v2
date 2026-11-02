def route_decision_prompt(best_route, rejected_routes):
    return f"""
You are an AI logistics decision system.

Chosen Route:
- Route ID: {best_route['route_id']}
- ETA: {best_route['eta_min']} minutes
- Fuel Cost: ₹{best_route['fuel_cost']}
- CO₂ Emission: {best_route['co2_kg']} kg
- 
- Total Loss: ₹{best_route['total_loss']}

Rejected Routes:
{rejected_routes}

Explain in simple business language:
- Why this route was chosen
- Why other routes were rejected
- What trade-offs were considered
- What risks were minimized
"""

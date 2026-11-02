def predict_carbon(fuel_liters):
    """
    Estimate CO₂ emissions in kg from fuel consumption (diesel assumed).
    Conversion: 1 liter diesel ≈ 2.68 kg CO₂
    """
    return fuel_liters * 2.68

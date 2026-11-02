class Vehicle:
    def __init__(self, vehicle_id, mileage_kmpl):
        self.vehicle_id = vehicle_id
        self.mileage_kmpl = mileage_kmpl
        self.fuel_price = 0.0

    def fuel_required(self, distance_km):
        return distance_km / self.mileage_kmpl

    def fuel_cost(self, distance_km):
        return self.fuel_required(distance_km) * self.fuel_price

from twin_state import TwinState
from route_model import Route
from vehicle_model import Vehicle
from subscriber import RedisSubscriber
from updater import apply_event

# Initialize twin
twin = TwinState()

# Static initialization (later from DB)
twin.routes["A-B"] = Route("A-B", 120)
twin.routes["B-C"] = Route("B-C", 90)

twin.vehicles["V1"] = Vehicle("V1", mileage_kmpl=5.5)

subscriber = RedisSubscriber()

print("🚀 Digital Twin started...")

for event in subscriber.listen():
    apply_event(event, twin)

    print("🧠 Twin State Updated")
    for r in twin.routes.values():
        print(f"{r.route_id} → {r.effective_distance:.2f} km")

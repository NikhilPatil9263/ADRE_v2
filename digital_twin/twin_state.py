from datetime import datetime

class TwinState:
    def __init__(self):
        self.routes = {}
        self.vehicles = {}
        self.last_update = None

    def update_timestamp(self):
        self.last_update = datetime.utcnow().isoformat()


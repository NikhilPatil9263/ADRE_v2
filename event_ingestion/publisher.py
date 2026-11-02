import redis
import json

class EventPublisher:
    def __init__(self, host='localhost', port=6379, db=0):
        self.r = redis.Redis(host=host, port=port, db=db)

    def publish_event(self, event):
        self.r.publish("ad_realtime_events", json.dumps(event))

import redis
import json

class RedisSubscriber:
    def __init__(self, channel="ad_realtime_events"):
        self.redis = redis.Redis(host="localhost", port=6379, decode_responses=True)
        self.pubsub = self.redis.pubsub()
        self.pubsub.subscribe(channel)

    def listen(self):
        for message in self.pubsub.listen():
            if message["type"] == "message":
                yield json.loads(message["data"])

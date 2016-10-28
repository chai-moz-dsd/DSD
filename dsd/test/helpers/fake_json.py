import json

class FakeJSON():
    @classmethod
    def load(cls):
        return json.dump({})
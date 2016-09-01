class FakeCache():
    @classmethod
    def get(key):
        if key == "refresh_token":
            return "929a3cec-16b5-47bc-87c7-e90e6fbc8207"

    @classmethod
    def set(cls, key, value, expire_time):
        return 0

class FakeCache():
    @classmethod
    def get(cls, key):
        if key == "refresh_token":
            return None

    @classmethod
    def set(cls, key, value, expire_time):
        if key == "refresh_token":
            return 0

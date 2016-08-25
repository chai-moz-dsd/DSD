from datetime import datetime


class FakeDatetime(datetime):

    @classmethod
    def now(cls, tz=None):
        return datetime(2016, 8, 25, 17, 43, 2, 387119).now()

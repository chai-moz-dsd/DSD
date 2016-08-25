from datetime import date


class FakeDate(date):
    @classmethod
    def today(cls):
        return cls(2016, 8, 25)

    @classmethod
    def build(cls, year, month, day):
        return date(year, month, day)

    def __str__(self):
        return "2016-08-25"

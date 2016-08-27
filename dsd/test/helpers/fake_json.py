from dsd.repositories.dhis2_oauth_token import REFRESH_TOKEN
import json
import uuid

class FakeJSON():
    @classmethod
    def load(cls, response):
        return json.dump({REFRESH_TOKEN:uuid.uuid4()})
import random
import string
import uuid


def generate_id():
    letter = random.choice(string.ascii_letters)
    id = "%s%s" % (letter, str(uuid.uuid4())[-10:])
    return id

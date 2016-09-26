import hashlib
import random
import string
import uuid


def generate_id():
    letter = random.choice(string.ascii_letters)
    id = "%s%s" % (letter, str(uuid.uuid4())[-10:])
    return id


def generate_md5_id(str):
    md5 = hashlib.md5(str.encode('utf-8'))
    return "%s%s" % ('o', md5.hexdigest()[-10:])

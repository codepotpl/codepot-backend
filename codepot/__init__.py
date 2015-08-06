import random
import string


def create_hash(length=32, char_set=string.ascii_letters + string.digits):
    return str(''.join(random.choice(char_set) for _ in range(length)))


def enum_to_model_choices(enum):
    return [(s.value, s.value) for s in enum]


def primary_key(length=10, char_set=string.ascii_letters + string.digits):
    return create_hash(length, char_set)


def int_primary_key(length=10):
    return int(create_hash(length, char_set=string.digits))

import random
import string


def create_hash(length=32, char_set=string.ascii_letters + string.digits):
    return str(''.join(random.choice(char_set) for _ in range(length)))


def enum_to_model_choices(enum):
    return [(s.value, s.value) for s in enum]

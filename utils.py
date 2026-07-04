import random
from config import RANDOM_NICKNAMES

def generate_random_name():
    """Selects a random name for bloated channels."""
    return random.choice(RANDOM_NICKNAMES")

def get_random_string(min_length=5, max_length=15):
    """Generates a pseudo-random string if needed for extra flair."""
    import random
    import string
    letters = string.ascii_lowercase + string.digits
    return ''.join(random.choice(letters) for i in range(random.randint(min_length, max_length)))

def generate_channel_name():
    """Combines name generation techniques."""
    base_name = generate_random_name()
    suffix = f"_{get_random_string(2, 4)}"
    return base_name + suffix

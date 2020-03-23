import random
import string

def random_id(n):
    """Generate a random alphanumeric string of length n"""
    chars = string.ascii_letters + string.digits
    return "".join(random.choice(chars) for _ in range(n))

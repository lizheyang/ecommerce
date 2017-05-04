import random


def generate_order_id():
    temp = [str(random.randrange(10)) for i in range(10)]
    return ''.join(temp)


cache = {}


def add(key, value):
    cache[key] = value


def remove(key):
    cache[key] = None
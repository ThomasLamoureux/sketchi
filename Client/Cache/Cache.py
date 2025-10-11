

cache = {}


def add(key, value):
    cache[key] = value


def get(key):
    return cache[key]


def remove(key):
    cache[key] = None


cache = {}


def add(key, value):
    cache[key] = value


def get(key):
    try:
        return cache[key]
    except KeyError:
        return None
    


def remove(key):
    try:
        del cache[key]      
    except KeyError:
        pass
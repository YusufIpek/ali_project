def get_watches(data):
    return list(filter(lambda x: x["group"].lower() == "watches" or x["group"].lower() == "uhren", data))


def get_specific_brands(data, *args):
    args = list(map(lambda x: x.lower(), args))
    return list(filter(lambda x: x["name"].lower() in args, data))


def drop_specific_brands(data, *args):
    args = list(map(lambda x: x.lower(), args))
    return list(filter(lambda x: x["name"].lower() not in args, data))


def get_items_with_attributes(data):
    return list(filter(lambda x: len(x.attributes) > 0, data))

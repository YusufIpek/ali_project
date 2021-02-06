def get_watches(data):
    return list(filter(lambda x: x["group"] == "WATCHES", data))

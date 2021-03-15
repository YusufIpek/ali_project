from typing import List
from dropshipping_item import DropshippingItem


def get_watches_and_jewelry(data):
    groups = ["schmuck", "uhren", "watches", "jewelry"]
    return list(filter(lambda x: x["group"].lower().strip() in groups, data))


def keep_only_adult_products(data: List[DropshippingItem]):
    groups = ["frau", "mann", "unisex"]
    result = []
    for item in data:
        found = list(
            filter(lambda x: x["group_name"] == "Geschlecht", item.attributes))
        if len(found) > 0:
            if found[0]["value_name"].lower() in groups:
                result.append(item)
    return result


def get_specific_brands(data, *args):
    args = list(map(lambda x: x.lower(), args))
    return list(filter(lambda x: x["name"].lower() in args, data))


def drop_specific_brands(data, *args):
    args = list(map(lambda x: x.lower(), args))
    return list(filter(lambda x: x["name"].lower() not in args, data))


def get_items_with_attributes(data):
    return list(filter(lambda x: len(x.attributes) > 0, data))

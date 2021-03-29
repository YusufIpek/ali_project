from typing import List
from dropshipping_item import DropshippingItem
import utils


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


def keep_only_products_with_images(data: List[DropshippingItem]):
    return list(filter(lambda x: '.jpg' in x.image_path.lower() and 'noimage' not in x.image_path.lower(), data))


def get_specific_brands(data, *args):
    args = list(map(lambda x: x.lower(), args))
    return list(filter(lambda x: x["name"].lower() in args, data))


def keep_only_specific_brands(data):
    uhren = ['armani exchange', 'bmw', 'diesel', 'emporio armani', 'fossil', 'guess', 'michael kors',
             'tommy hilfinger', 'pierre cardin', 'citizen', 'calvin klein']
    schmuck = ['armani emporio', 'esprit', 'fossil', 'guess', 'pierre cardin', 'michael kors',
               'swarovski', 'tommy hilfiger']

    return list(filter(lambda x: x["group"].lower().strip() == 'uhren' and utils.brand_equal_check_special_solution(x["name"].lower().strip(), uhren)
                       or x["group"].lower().strip() == 'schmuck' and utils.brand_equal_check_special_solution(x["name"].lower().strip(), schmuck), data))


def drop_specific_brands(data, *args):
    args = list(map(lambda x: x.lower(), args))
    return list(filter(lambda x: x["name"].lower() not in args, data))


def get_items_with_attributes(data):
    return list(filter(lambda x: len(x.attributes) > 0, data))

from typing import List
from dropshipping_item import DropshippingItem
import utils


def get_watches_and_jewelry(data, jewelry_add=True):
    watch = ["uhren", "watches"]
    jewelry = ["schmuck", "jewelry"]
    groups = []
    groups.extend(watch)
    if jewelry_add:
        groups.extend(jewelry)

    return list(filter(lambda x: x["group"].lower().strip() in groups, data))


def keep_only_adult_products(data: List[DropshippingItem]):
    groups = ["frau", "mann", "unisex"]
    result = []
    for item in data:
        found = list(filter(lambda x: x["group_name"] == "Geschlecht", item.attributes))
        if len(found) > 0:
            if found[0]["value_name"].lower() in groups:
                result.append(item)
    return result


def keep_only_products_with_images(data: List[DropshippingItem]):
    return list(
        filter(
            lambda x: ".jpg" in x.image_path.lower()
            and "noimage" not in x.image_path.lower(),
            data,
        )
    )


def get_specific_brands(data, *args):
    args = list(map(lambda x: x.lower(), args))
    return list(filter(lambda x: x["name"].lower() in args, data))


def keep_only_specific_brands(data):
    uhren = [
        "guess",
        "guess collection",
        "guess 2013",
        "guess connect",
        "pierre cardin",
        "citizen",
        "ck calvin klein neue kollektion",
        "liebeskind berlin",
        "police",
        "breil",
        "casio",
        "casio eu",
        "seiko",
        "timex",
        "esprit",
        "just cavalli time uhren",
        "bering",
        "armani exchange connected",
        "emporio armani",
        "emporio armani connected",
        "emporio armani swiss made",
        "marc ecko",
        "marc ecko neue kollektion",
        "pierre lannier",
        "tommy hilfiger",
        "puma smartwatch",
        "dkny smartwatch",
    ]
    schmuck = []

    return list(
        filter(
            lambda x: x["group"].lower().strip() == "uhren"
            and utils.brand_equal_check_special_solution(
                x["name"].lower().strip(), uhren
            )
            or x["group"].lower().strip() == "schmuck"
            and utils.brand_equal_check_special_solution(
                x["name"].lower().strip(), schmuck
            ),
            data,
        )
    )


def remove_watches_by_reference(data: List[DropshippingItem]):
    references_to_remove = [
        "GW0109L2",
        "GW0111L2",
        "GW0214G1",
        "GW0214G2",
        "GW0243L3",
        "GW0248G2",
        "GW0254L1",
        "GW0257L1",
        "GW0260G1",
        "GW0262G2",
        "GW0263G2",
        "W0380G4",
        "W0659G4",
        "W0660G2",
        "W0874G1",
        "W0972G1",
        "W0990G1",
        "W0991G7",
        "W1049G3",
        "W1041G2",
        "W1050G1",
        "W1075G1",
        "W1093L1",
        "W1159L1",
        "W1180G1",
        "ESRG00961117",
        "ESRG00961118",
        "15032_1",
        "10141_2",
        "15150_A",
        "15151_A",
        "18240_1",
        "18678_A",
        "18678_B",
        "18678_C",
        "18678_D",
        "18678_E",
        "18678_F",
        "18679_A",
        "18679_B",
        "18679_C",
        "18679_D",
        "18679_E",
        "18679_F",
        "18758_2",
    ]
    return list(filter(lambda x: x.reference not in references_to_remove, data))


def drop_specific_brands(data, *args):
    args = list(map(lambda x: x.lower(), args))
    return list(filter(lambda x: x["name"].lower() not in args, data))


def keep_items_with_attributes(data):
    brands_not_touch = ["pierre cardin"]
    return list(
        filter(
            lambda x: utils.brand_equal_check_special_solution(
                x.brand_name.lower().strip(), brands_not_touch
            )
            or len(x.attributes) > 0,
            data,
        )
    )

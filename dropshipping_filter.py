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


def keep_only_specific_brands(
    brands, uhren: List[str], schmuck=[], include_all_smartwatches=True
):

    # keep specified brands and keep all smart watches
    tmpList = list(
        filter(
            lambda x: x["group"].lower().strip() == "uhren"
            and utils.brand_equal_check_special_solution(
                x["name"].lower().strip(), uhren
            )
            or x["group"].lower().strip() == "schmuck"
            and utils.brand_equal_check_special_solution(
                x["name"].lower().strip(), schmuck
            ),
            brands,
        )
    )
    if include_all_smartwatches:
        return list(
            filter(lambda x: x["category"].lower().strip() == "smart uhren", tmpList)
        )
    return tmpList


def filter_smartwatches(products: List[DropshippingItem], uhren: List[str], schmuck=[]):
    # in the products we have also products from brands which were not specified, because we wanted to retrieve also all
    # smartwatches, thus here we remove watches which are not specified in the brands list and are not smart watches

    return list(
        filter(
            lambda x: utils.brand_equal_check_special_solution(
                x.category_object["name"].lower().strip(), uhren
            )
            or utils.brand_equal_check_special_solution(
                x.category_object["name"].lower().strip(), schmuck
            )
            or x.is_product_smartwatch(),
            products,
        )
    )


def remove_watches_by_reference(data: List[DropshippingItem]):
    references_to_remove = []
    with open("watches_delete.txt", "r") as f:
        references_to_remove = f.read().splitlines()

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

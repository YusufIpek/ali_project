from dropshipping_item import DropshippingItem
from dropshipping_filter import drop_specific_brands, get_specific_brands, get_watches
from utils import *
import requests
import json

requests.packages.urllib3.disable_warnings()


def init():
    with open("config.json") as json_file:
        config = json.load(json_file)
    global api_info, user_info
    api_info = config["api_info"]
    user_info = config["user_info"]


def data_payload(request_type, **kwargs):
    data = {
        "uid": user_info["uid"],
        "pid": user_info["pid"],
        "lid": user_info["lid"],
        "key": user_info["key"],
        "request": request_type,
        "api_version": api_info["version"]

    }
    if kwargs.get("id_brand") is not None:
        data["id_brand"] = kwargs.get("id_brand")
        data["display_attributes"] = True
    if kwargs.get('id_product') is not None:
        data["id_product"] = kwargs.get("id_product")
        data["display_attributes"] = True

    payload = {
        "data": json.dumps(data)
    }

    return payload


def make_request(payload):
    response = requests.post(api_info["url"], data=payload, verify=False)
    if response.status_code is not 200:
        exit("Dropshipping API Aufruf ist fehlgeschlagen!")
    return response.content


def get_brands():
    request_type = "get_brands"
    payload = data_payload(request_type)
    return make_request(payload)


def get_brands_items(id_brand):
    request_type = "get_brand_items"
    payload = data_payload(request_type, id_brand=id_brand)
    return make_request(payload)


def brands_items_to_list(all_brands, limit=-1, keep_empty_attributes=True):
    size = limit if limit > -1 else len(all_brands)
    print(f"get watches from {size} brands...")

    if limit is not -1 and limit > 0:
        all_brands = all_brands[:size]

    items = []
    for index, brand in enumerate(all_brands):
        print(f"processing {index+1}/{len(all_brands)}")
        response = get_brands_items(brand["id_brand"])
        parsed_response = parse_response(response)
        if parsed_response["num_rows"] > 0:
            items.extend(parsed_response["rows"])

    filtered = list(filter(lambda x: "icon_path" in x, items))
    mapped = list(map(lambda x: DropshippingItem(x), filtered))
    for item in mapped:
        item.image_base64 = get_item_image(item.image_path)

    if not keep_empty_attributes:
        mapped = list(filter(lambda x: x.attributes_available(), mapped))

    print(f"{len(mapped)} products retrieved from {size} brands")
    return mapped


def get_item(id_product):
    request_type = "get_item"
    payload = data_payload(request_type, id_product=id_product)
    return make_request(payload)


def product_items_to_list(brands_items, keep_empty_attributes=True):
    print("product items to list:")

    items = []
    for index, item in enumerate(brands_items):
        print(str(index) + "/" + str(len(brands_items)))
        response = parse_response(get_item(item["id_product"]))
        if response["num_rows"] > 0:
            if "image_path" in response["rows"][0]:
                item = DropshippingItem(response["rows"][0])
            else:
                continue

            try:
                item.image_base64 = get_item_image(item.image_path)
            except Exception as e:
                print("image couldn't be created for" + item.name)
                print(item)
                print(e)

            if keep_empty_attributes or item.attributes_available():
                items.append(item)
    return items


def get_item_image(url):
    response = requests.get(url)
    return image_byte_to_base64(response.content).decode('utf-8')


if False:
    # read config data and initialize api and user object
    init()

    # get all brands
    all_brands = get_brands()
    write_to_file("response/brands.json", all_brands)

    # filter get only watches
    filtered_categories = get_watches(parse_response(all_brands)["rows"])
    filtered_categories_in_byte = json.dumps(
        filtered_categories).encode('utf-8')
    write_to_file("response/filtered_categories.json",
                  filtered_categories_in_byte)

    filtered_brands = drop_specific_brands(
        filtered_categories, "disney")
    filtered_brands_in_byte = json.dumps(filtered_brands).encode('utf-8')
    write_to_file("response/filtered_brands.json", filtered_brands_in_byte)

    # get all items of watches
    all_items = brands_items_to_list(
        filtered_brands, keep_empty_attributes=False)
    # all_items_in_byte = json.dumps(all_items).encode('utf-8')
    # write_to_file("response/filtered_brands_items.json", all_items_in_byte)
    write_multiple_files(all_items)

    # # get detailed product info
    # all_items_info = product_items_to_list(all_items, False)
    # write_multiple_files(all_items_info)

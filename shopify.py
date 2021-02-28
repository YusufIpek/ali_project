from dropshipping_item import DropshippingItem
import json
import requests
from utils import *

# group all products in the collection
collection = 237585006758


def init():
    with open("config.json") as file:
        config = json.load(file)

    global shopify
    shopify = config["shopify"]


def do_get_request(req_url, is_relative_path=True):
    headers = {
        "X-Shopify-Access-Token": shopify["key"]
    }
    if is_relative_path:
        return requests.get(shopify["url"] + req_url, headers=headers)
    else:
        return requests.get(req_url, headers=headers)


def do_post_request(req_url, data):
    headers = {
        "X-Shopify-Access-Token": shopify["key"],
        "Content-Type": "application/json"
    }
    return requests.post(shopify["url"] + req_url, headers=headers, json=data)


def do_put_request(req_url, data):
    headers = {
        "X-Shopify-Access-Token": shopify["key"],
        "Content-Type": "application/json"
    }
    return requests.put(shopify["url"] + req_url, headers=headers, json=data)


def get_products():
    req_url = "admin/api/2021-01/products.json"
    response = do_get_request(req_url)
    return response.content


def get_products_of_dropshipping(collection_id, previous_response=None):
    # this request uses pagination, max limit is 250, default is 50, if there
    # are further products available we get the property link in the response,
    # which contains the next url to get the next products
    # read more here: https://shopify.dev/tutorials/make-paginated-requests-to-rest-admin-api
    is_relative = True
    if previous_response:
        req_url = previous_response.links["next"]["url"]
        is_relative = False
    else:
        req_url = f"/admin/api/2021-01/collections/{collection_id}/products.json"
    response = do_get_request(req_url, is_relative_path=is_relative)
    return response


def get_location():
    req_url = "/admin/api/2021-01/locations.json"
    response = do_get_request(req_url)
    return response.content


def add_product(item: DropshippingItem):
    req_url = "/admin/api/2021-01/products.json"
    product = {
        "product": {
            "title": item.name,
            "vendor": item.brand_name,
            "body_html": attributes_to_html(item.attributes),
            "product_type": item.get_gender(),
            "images": [
                {
                    "attachment": item.image_base64
                }
            ],
            "shop": {
                "id": 50964234406,
                "currency": "EUR"
            },
            "published_scope": "web"
        }
    }
    response = do_post_request(req_url, product)
    return response


def add_product_to_collect(product_id):
    req_url = "/admin/api/2021-01/collects.json"
    data = {
        "collect": {
            "product_id": product_id,
            "collection_id": 237585006758   # dropshipping category
        }
    }
    response = do_post_request(req_url, data)
    return response


def get_all_collections():
    req_url = "/admin/api/2021-01/custom_collections.json"
    response = do_get_request(req_url)
    return response


def get_collection_dropshipping_id():
    response = get_all_collections()
    parsed_response = parse_response(response.content)
    coll_dropshipping = list(filter(lambda x: x["title"].lower(
    ) == "dropshipping", parsed_response["custom_collections"]))
    return coll_dropshipping[0]["id"]


def get_field_from_response(response, field: str):
    resp = parse_response(response)
    return resp['product'][field]


def set_price_of_product(id, price):
    req_url = "admin/api/2021-01/variants/" + str(id) + ".json"
    data = {
        "variant": {
            "id": id,
            "inventory_management": "shopify",
            "price": str(price)
        }
    }
    response = do_put_request(req_url, data)
    return response


def set_inventory_of_product(inventory_item_id: int, stock: int):
    location_response = get_location()
    locations = parse_response(location_response)
    location_id = locations["locations"][0]["id"]
    req_url = "admin/api/2021-01/inventory_levels/set.json"
    data = {
        "location_id": location_id,
        "inventory_item_id": inventory_item_id,
        "available": stock
    }
    response = do_post_request(req_url, data)
    return response


if False:
    init()
    dropshipping_collection_id = get_collection_dropshipping_id()
    response = get_products_of_dropshipping(dropshipping_collection_id)
    parsed_products = parse_response(response.content)
    print(len(parsed_products["products"]))

    print(len(parse_response(get_products_of_dropshipping(
        dropshipping_collection_id, response).content)["products"]))

    # products = get_products()
    # write_to_file("response/shopify.json", products)

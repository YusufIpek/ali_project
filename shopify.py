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


def do_get_request(req_url):
    headers = {
        "X-Shopify-Access-Token": shopify["key"]
    }
    return requests.get(shopify["url"] + req_url, headers=headers)


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
            "body_html": f'<p>{item.brand_name}</p>',
            "product_type": 'Herren',
            "images": [
                {
                    "attachment": item.image_base64
                }
            ],
            "shop": {
                "id": 50964234406,
                "currency": "EUR"
            },
            "published": False,
            "status": "draft"
        }
    }
    response = do_post_request(req_url, product)
    return response


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


init()
products = get_products()
write_to_file("response/shopify.json", products)

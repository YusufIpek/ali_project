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


def get_products():
    req_url = "admin/api/2021-01/products.json"
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
            "variants": [{
                "option1": "Standard",
                "price": item.price,
                "currency_code": "EUR",
                "sku": "Test"
            }],
            "published": False
        }
    }
    response = do_post_request(req_url, product)
    print(response.headers)
    print(response.status_code)
    print(response.content)


init()
products = get_products()
write_to_file("response/shopify.json", products)

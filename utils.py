from typing import List
from dropshipping_item import DropshippingItem
import json
import base64
from json.encoder import JSONEncoder
import copy
from datetime import date, datetime
import os
import re


class ItemEncoder(JSONEncoder):
    def default(self, o):
        if isinstance(o, DropshippingItem):
            tmp = copy.deepcopy(o)
            delattr(tmp, 'image_base64')
        return tmp.__dict__


def parse_response(content):
    return json.loads(content)


def write_to_file(filename, content, as_byte=True):
    create_folder_if_not_exist('response')
    if as_byte:
        with open('response/' + filename, "wb") as f:
            f.write(content)
    else:
        if isinstance(content, dict):
            with open('response/' + filename, "w") as f:
                f.write(json.dumps(content))
        else:
            with open('response/' + filename, "w") as f:
                f.write(json.dumps(content, cls=ItemEncoder))


def write_multiple_files(items):
    create_folder_if_not_exist('response')
    for item in items:
        write_to_file("response/"+item.id_product + ".json",
                      json.dumps(item.__dict__).encode('utf-8'))


def image_byte_to_base64(image):
    return base64.b64encode(image)


def attributes_to_html(dropshippingItem: DropshippingItem):
    html = "<h2 class=\"spr-header-title\">Produktdetails</h2>"
    html += "<div class=\"row\">"
    html += f"<div class=\"col-6 bg-light'\">Modellnummer</div>"
    html += f"<div class=\"col-6 bg-light'\">{dropshippingItem.reference}</div>"

    for index, item in enumerate(dropshippingItem.attributes):
        html += f"<div class=\"col-6 {'bg-light' if index%2 == 0 else ''}\">{item['group_name']}</div>"
        html += f"<div class=\"col-6 {'bg-light' if index%2 == 0 else ''}\">{ item['value_name'] }</div>"
        html += "<div class=\"w-100\"></div>"
    html += "</div>"
    return html


def get_date():
    return str(date.today())


def dropshipping_products_to_csv(data: List[DropshippingItem], output):
    with open('response/' + output + '.txt', 'w+') as f:
        for item in data:
            f.writelines(
                f'{item.name},{item.category_object["group"]},{item.retail_price},{item.discount},{item.price},{item.get_selling_price()}\n')


def price_comparison(data, output):
    with open('response/' + output + '.txt', 'w+') as f:
        for item in data:
            f.writelines(
                f'{item["title"]},{item["product_type"]},{item["variants"][0]["price"]},{item["new_price"]}\n')


def get_timestamp():
    return str(datetime.now()).replace(":", "-")


def create_folder_if_not_exist(folder_name):
    if not os.path.exists(folder_name):
        os.mkdir(folder_name)


def brand_equal_check_special_solution(input, collection):
    found = list(filter(lambda x: x == input, collection))
    if len(found):
        return True
    return False


def get_dropshipping_id_from_shopify_product(shopify_item):
    return re.findall(r'\d+', shopify_item['tags'])[0]

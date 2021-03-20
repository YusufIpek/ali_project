from dropshipping_item import DropshippingItem
import json
import base64
from json.encoder import JSONEncoder
import copy
from datetime import date, datetime
import os


class ItemEncoder(JSONEncoder):
    def default(self, o):
        if isinstance(o, DropshippingItem):
            tmp = copy.deepcopy(o)
            delattr(tmp, 'image_base64')
        return tmp.__dict__


def parse_response(content):
    return json.loads(content)


def write_to_file(filename, content, as_byte=True):
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
    for item in items:
        write_to_file("response/"+item.id_product + ".json",
                      json.dumps(item.__dict__).encode('utf-8'))


def image_byte_to_base64(image):
    return base64.b64encode(image)


def attributes_to_html(attributes):
    html = "<h2 class=\"spr-header-title\">Produktdetails</h2>"
    html += "<div class=\"row\">"
    for index, item in enumerate(attributes):
        html += f"<div class=\"col-6 {'bg-light' if index%2 == 0 else ''}\">{item['group_name']}</div>"
        html += f"<div class=\"col-6 {'bg-light' if index%2 == 0 else ''}\">{ item['value_name'] }</div>"
        html += "<div class=\"w-100\"></div>"
    html += "</div>"
    return html


def get_date():
    return str(date.today())


def get_timestamp():
    return str(datetime.now()).replace(":", "-")


def create_folder_if_not_exist(folder_name):
    if not os.path.exists(folder_name):
        os.mkdir(folder_name)


def brand_equal_check_special_solution(input, collection):
    tmp = input.split(" ")
    for t in tmp:
        for c in collection:
            if t == c:
                return True
    return False

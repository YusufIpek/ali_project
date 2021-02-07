import json
import base64


def parse_response(content):
    return json.loads(content)


def write_to_file(filename, content):
    with open(filename, "wb") as f:
        f.write(content)


def write_multiple_files(items):
    for item in items:
        write_to_file("response/"+item.id_product + ".json",
                      json.dumps(item.__dict__).encode('utf-8'))


def image_byte_to_base64(image):
    return base64.b64encode(image)

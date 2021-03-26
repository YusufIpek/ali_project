

from dropshipping_filter import keep_only_specific_brands
from utils import parse_response


if __name__ == '__main__':
    items = {}
    with open('response/all_brands.json', 'r') as f:
        items = parse_response(f.read())

    result = keep_only_specific_brands(items)
    print(len(result))

    for item in result:
        print(item["name"])

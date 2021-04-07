

from dropshipping_filter import keep_only_specific_brands
from utils import parse_response


if __name__ == '__main__':
    items = {}
    with open('response/all_brands.json', 'r') as f:
        items = parse_response(f.read())

    result = keep_only_specific_brands(items)

    uhren = ['guess', 'tommy hilfiger', 'pierre cardin', 'citizen', 'calvin klein',
             'lacoste', 'liebeskind', 'nautica', 'olivia burton', 'police', 'breil']
    schmuck = ['esprit', 'guess', 'pierre cardin',
               'swarovski', 'tommy hilfiger']

    tmp_set = list(map(lambda x: x["name"].lower().strip(), result))
    print("uhren check...")
    for item in uhren:
        found = list(filter(lambda x: item in x, tmp_set))
        if len(found) == 0:
            print(f"uhr: {item} is not added")

    print("schmuck check...")
    for item in schmuck:
        found = list(filter(lambda x: item in x, tmp_set))
        if len(found) == 0:
            print(f"schmuck: {item} is not added")

    print(len(result))

    for item in result:
        print(item["name"])



from dropshipping_filter import keep_only_specific_brands
from utils import parse_response


if __name__ == '__main__':
    items = {}
    with open('response/all_brands.json', 'r') as f:
        items = parse_response(f.read())

    result = keep_only_specific_brands(items)

    uhren = ['guess', 'guess collection', 'guess 2013', 'guess connect', 'pierre cardin', 'citizen', 'ck calvin klein neue kollektion',
             'liebeskind berlin', 'nautica', 'police', 'breil', 'casio', 'casio eu',
             'seiko', 'timex', 'festina', 'esprit', 'just cavalli time uhren', 'lotus']
    schmuck = ['esprit', 'guess schmuck', 'guess steel', 'guess neue kollektion', 'pierre cardin jewels',
               'swarovski jewels']

    tmp_set = list(map(lambda x: x["name"].lower().strip(), result))
    print("uhren check if brand not available...")
    for item in uhren:
        found = list(filter(lambda x: item in x, tmp_set))
        if len(found) == 0:
            print(f"----- {item} is not in the collection!!!!")

    print("schmuck check if brand not available...")
    for item in schmuck:
        found = list(filter(lambda x: item in x, tmp_set))
        if len(found) == 0:
            print(f"----- {item} is not in the collection!!!!")

    print('printing all brands')
    print(len(result))

    for item in result:
        print(item["name"])

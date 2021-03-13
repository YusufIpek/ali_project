from dropshipping_item import DropshippingItem
from typing import List
from utils import parse_response, write_multiple_files, write_to_file
import dropshipping
import shopify

# load credentials
dropshipping.init()
shopify.init()


def get_all_products_from_dropshipping(persist=False):
    # get all brands
    all_brands = dropshipping.get_brands()

    # filter get only watches
    filtered_brands = dropshipping.get_watches(
        dropshipping.parse_response(all_brands)["rows"])

    # get all items of watches
    all_items = dropshipping.brands_items_to_list(filtered_brands, 3, False)

    if persist:
        write_to_file('dropshipping_products.json', all_items, False)

    return all_items


def get_all_watches_from_shopify(persist):
    # get all dropshipping products from shopify
    # dropshipping_collection_id = shopify.get_collection_dropshipping_id()
    # response = shopify.get_products_of_dropshipping(dropshipping_collection_id)
    # watches_from_shopify = parse_response(response.content)

    response = shopify.get_products()
    response = parse_response(response)
    result = list(
        filter(lambda x: 'dropshipping' in x['tags'], response['products']))

    if persist:
        write_to_file('shopify_dropshipping_products.json',
                      result, False)

    return result


def check_quantity_match(dropshipping_products: List[DropshippingItem], shopify_products):
    for shopify_item in shopify_products:
        dropshipping_product_id = shopify_item['tags']
        result = list(filter(lambda x: x.id_product ==
                             dropshipping_product_id, dropshipping_products))
        print(result)


def add_product_if_not_present(dropshipping_products: List[DropshippingItem], shopify_products):
    print('adding products to shopify...')
    counter = 0
    for dropshipping_item in dropshipping_products:
        result = list(
            filter(lambda x: dropshipping_item.id_product in x['tags'], shopify_products))
        if len(result) == 0:
            # add product to shopify
            response = shopify.add_product(dropshipping_item)
            response = parse_response(response.content)

            # set price of product
            variants = response["product"]["variants"]
            shopify.set_price_of_product(
                variants[0]["id"], dropshipping_item.price)

            # set quantity of product
            inventory_item_id = variants[0]["inventory_item_id"]
            shopify.set_inventory_of_product(
                inventory_item_id, dropshipping_item.stock)

            # add product to collection ("dropshipping" category)
            shopify.add_product_to_collect(
                response["product"]["id"])

            counter += 1

    print(f"{counter} products added")


shopify_products = get_all_watches_from_shopify(False)
dropshipping_products = get_all_products_from_dropshipping(False)

add_product_if_not_present(dropshipping_products, shopify_products)

# get detailed product info | not required because we get from the above request also the product info
# all_items_info = ds.product_items_to_list(all_items)
# print("Amount of products to add:" + str(len(all_items)))

# for index, item in enumerate(all_items):
#     print("processing: " + str(index+1) + "/" + str(len(all_items)))
#     response = shopify.add_product(item)
#     write_to_file("response/shopify_response_" +
#                   str(index) + ".json", response.content)

#     # set price of product
#     response = parse_response(response.content)
#     variants = response["product"]["variants"]
#     update = shopify.set_price_of_product(variants[0]["id"], item.price)

#     # set quantity of product
#     inventory_item_id = variants[0]["inventory_item_id"]
#     inventory_response = shopify.set_inventory_of_product(
#         inventory_item_id, item.stock)

#     # add product to collection ("dropshipping" category)
#     added_to_collection = shopify.add_product_to_collect(
#         response["product"]["id"])

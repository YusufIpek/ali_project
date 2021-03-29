from dropshipping_item import DropshippingItem
from typing import List
from utils import dropshipping_products_to_csv, get_timestamp, parse_response, write_to_file
import dropshipping_filter
import dropshipping
import shopify
import re
from log_handler import *
import cProfile


def get_all_products_from_dropshipping(persist=False):
    # get all brands
    all_brands = dropshipping.get_brands()

    # filter get only watches
    filtered_brands = dropshipping_filter.get_watches_and_jewelry(
        dropshipping.parse_response(all_brands)["rows"])

    write_to_file('all_brands.json', filtered_brands, False)

    filtered_brands = dropshipping_filter.keep_only_specific_brands(
        filtered_brands)

    # get all items of watches
    all_items = dropshipping.brands_items_to_list(
        filtered_brands, limit=-1, keep_empty_attributes=True, generate_base64_image=False)

    # remove children products
    # all_items = dropshipping.keep_only_adult_products(all_items)

    all_items = dropshipping_filter.keep_only_products_with_images(all_items)

    if persist:
        write_to_file('dropshipping_products.json', all_items, False)

    return all_items


def get_all_watches_from_shopify(persist):
    # get all dropshipping products from shopify
    # dropshipping_collection_id = shopify.get_collection_dropshipping_id()
    # response = shopify.get_products_of_dropshipping(dropshipping_collection_id)
    # watches_from_shopify = parse_response(response.content)

    response = shopify.get_products()
    result = list(filter(lambda x: 'dropshipping' in x['tags'], response))

    if persist:
        write_to_file('shopify_dropshipping_products.json',
                      result, False)

    return result


def update_quantity_if_differ(dropshipping_products: List[DropshippingItem], shopify_products):
    logger.info("checking for product quantity difference...")
    count = 0

    for shopify_item in shopify_products:
        dropshipping_product_id = re.findall(
            r'\d+', shopify_item['tags'])[0]
        result = list(filter(lambda x: x.id_product ==
                             dropshipping_product_id, dropshipping_products))
        if len(result) > 0:
            shopify_quantity = shopify_item['variants'][0]['inventory_quantity']
            dropshipping_quantity = int(result[0].stock)
            if shopify_quantity is not dropshipping_quantity:
                logger.info(
                    f"updating product quantity of {shopify_item['title']} from {shopify_quantity} to {dropshipping_quantity}")
                # update quantity of product on shopify
                inventory_item_id = shopify_item['variants'][0]["inventory_item_id"]
                shopify.set_inventory_of_product(
                    inventory_item_id, result[0].stock)

                count += 1

    logger.info(f"quantity of {count} products updated")


def add_product_if_not_present(dropshipping_products: List[DropshippingItem], shopify_products):
    logger.info(f'adding products to shopify...')
    counter = 0
    for dropshipping_item in dropshipping_products:
        result = list(
            filter(lambda x: dropshipping_item.id_product == re.findall(
                r'\d+', x['tags'])[0], shopify_products))
        if len(result) == 0:
            logger.info(f'adding {dropshipping_item.name} to shopify')

            # add product to shopify
            response = shopify.add_product(dropshipping_item)
            response = parse_response(response.content)

            # set price of product
            variants = response["product"]["variants"]
            shopify.set_price_of_product(
                variants[0]["id"], dropshipping_item.get_selling_price())

            # set quantity of product
            inventory_item_id = variants[0]["inventory_item_id"]
            shopify.set_inventory_of_product(
                inventory_item_id, dropshipping_item.stock)

            # add product to collection ("dropshipping" category)
            shopify.add_product_to_collect(
                response["product"]["id"])

            counter += 1

    logger.info(f"{counter} products added")


def delete_product_if_not_available_on_dropshipping(dropshipping_products: List[DropshippingItem], shopify_products):
    logger.info("checking if product should be removed from shopify...")
    count = 0

    for shopify_item in shopify_products:
        dropshipping_product_id = re.findall(
            r'\d+', shopify_item['tags'])[0]
        result = list(filter(lambda x: x.id_product ==
                             dropshipping_product_id, dropshipping_products))
        if len(result) == 0:
            logger.info(f"deleting {shopify_item['title']}")
            shopify.delete_product(shopify_item['id'])
            count += 1

    logger.info(f"{count} products were deleted")


def main():
    try:
        # load credentials
        dropshipping.init()
        shopify.init()

        shopify_products = get_all_watches_from_shopify(False)
        dropshipping_products = get_all_products_from_dropshipping(False)

        write_to_file('shopify_products.json', shopify_products, False)
        write_to_file('dropshipping_products.json',
                      dropshipping_products, False)

        # dropshipping_products_to_csv(
        #     dropshipping_products, 'dropshipping_produkte')

        add_product_if_not_present(
            dropshipping_products, shopify_products)
        update_quantity_if_differ(dropshipping_products, shopify_products)
        delete_product_if_not_available_on_dropshipping(
            dropshipping_products, shopify_products)
    except:
        logger.exception('Exception occured')


if __name__ == '__main__':
    main()
    # uncomment below code to execute profiling
    # utils.create_folder_if_not_exist('profiling')
    # cProfile.run('main()', 'profiling/profiling_stats-' +
    #              get_timestamp() + '.stat')

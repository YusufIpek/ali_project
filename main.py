from utils import parse_response, write_multiple_files, write_to_file
import dropshipping
import shopify

# load credentials
dropshipping.init()
shopify.init()

# get all brands
all_brands = dropshipping.get_brands()

# filter get only watches
filtered_brands = dropshipping.get_watches(
    dropshipping.parse_response(all_brands)["rows"])

# get all items of watches
all_items = dropshipping.brands_items_to_list(filtered_brands, 3, False)
write_multiple_files(all_items)

# get detailed product info | not required because we get from the above request also the product info
# all_items_info = ds.product_items_to_list(all_items)

print("Amount of products to add:" + str(len(all_items)))

for index, item in enumerate([all_items[0]]):
    print("processing: " + str(index+1) + "/" + str(len(all_items)))
    response = shopify.add_product(item)
    write_to_file("response/shopify_response_" +
                  str(index) + ".json", response.content)

    # set price of product
    response = parse_response(response.content)
    variants = response["product"]["variants"]
    update = shopify.set_price_of_product(variants[0]["id"], item.price)

    # set quantity of product
    inventory_item_id = variants[0]["inventory_item_id"]
    inventory_response = shopify.set_inventory_of_product(
        inventory_item_id, item.stock)

    # add product to collection ("dropshipping" category)
    added_to_collection = shopify.add_product_to_collect(
        response["product"]["id"])

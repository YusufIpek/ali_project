from utils import parse_response, write_multiple_files, write_to_file
import dropshipping as ds
import shopify as sp

# load credentials
ds.init()
sp.init()

# get all brands
all_brands = ds.get_brands()

# filter get only watches
filtered_brands = ds.get_watches(ds.parse_response(all_brands)["rows"])

# get all items of watches
all_items = ds.brands_items_to_list(filtered_brands, 1)
write_multiple_files(all_items)

# get detailed product info
# all_items_info = ds.product_items_to_list(all_items)

for index, item in enumerate(all_items):
    response = sp.add_product(item)
    write_to_file("response/shopify_response_" +
                  str(index) + ".json", response.content)

    response = parse_response(response.content)
    variants = response["product"]["variants"]
    update = sp.set_price_of_product(variants[0]["id"], item.price)

    inventory_item_id = variants[0]["inventory_item_id"]

    inventory_response = sp.set_inventory_of_product(
        inventory_item_id, item.stock)

    added_to_collection = sp.add_product_to_collect(response["product"]["id"])
    break

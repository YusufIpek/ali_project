from utils import write_to_file
import dropshipping as ds
import shopify as sp

ds.init()

# get all brands
all_brands = ds.get_brands()

# filter get only watches
filtered_brands = ds.get_watches(ds.parse_response(all_brands)["rows"])

# get all items of watches
all_items = ds.brands_items_to_list(filtered_brands)

# get detailed product info
all_items_info = ds.product_items_to_list(all_items)

response = sp.add_product(all_items_info[0])
write_to_file("response/shopify_response.json", response.content)

variants = sp.get_field_from_response(response.content, 'variants')
update = sp.update_product(variants[0]["id"], all_items_info[0].price)

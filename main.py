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

sp.add_product(all_items_info[0])

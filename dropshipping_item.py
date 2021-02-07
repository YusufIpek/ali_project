

class DropshippingItem:
    def __init__(self, data):
        self.id_product = data["id_product"]
        self.reference = data["reference"]
        self.brand_name = data["brand_name"]
        self.name = data["name"]
        self.stock = data["stock"]
        self.weight = data["weight"]
        self.retail_price = data["retail_price"]
        self.discount = data["discount"]
        self.price = data["price"]
        self.id_supplier = data["id_supplier"]
        self.speed_shipping = data["speed_shipping"]
        self.ean = data["ean"]
        self.icon_path = data["icon_path"]
        self.image_path = data["image_path"]
        self.image_last_update = data["image_last_update"]
        self.currency = data["currency"]
        self.image_base64 = ""

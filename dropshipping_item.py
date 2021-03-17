

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
        self.price = data["retail_price"] if data["retail_price"] is not data["price"] else str(
            int(data["retail_price"]) * 1.3)
        self.id_supplier = data["id_supplier"]
        self.speed_shipping = data["speed_shipping"]
        self.ean = data["ean"]
        self.icon_path = data["icon_path"]
        self.image_path = data["image_path"]
        self.image_last_update = data["image_last_update"]
        self.currency = data["currency"]
        self.attributes = data["attributes_array"]
        self.image_base64 = ""

    def attributes_available(self):
        return len(self.attributes) > 0

    def get_gender(self):
        mapping = {
            "mann": "Herren",
            "frau": "Damen",
            "unisex": "Damen & Herren",
            "kind": "Kind"
        }
        found = list(
            filter(lambda x: x["group_name"].lower() == 'geschlecht', self.attributes))

        if len(found) > 0:
            return mapping[found[0]["value_name"].lower()]
        else:
            return None

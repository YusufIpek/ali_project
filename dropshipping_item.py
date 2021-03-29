class DropshippingItem:
    def __init__(self, data, category):
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
        self.attributes = data["attributes_array"]
        self.image_base64 = ""
        self.category_object = category

    def attributes_available(self):
        return len(self.attributes) > 0

    def get_product_type(self):
        mapping = {
            "mann": "Herren",
            "frau": "Damen",
            "unisex": "Unisex",
            "kind": "Kind"
        }
        found = list(
            filter(lambda x: x["group_name"].lower() == 'geschlecht', self.attributes))

        if len(found) > 0:
            return mapping[found[0]["value_name"].lower()] + self.category_object["group"].strip()
        else:
            return "Unbekannt" + self.category_object["group"].strip()

    def get_title(self):
        # if self.brand_name.lower().strip() == 'guess':
        if self.reference in self.name:
            return self.name
        return self.name + " - " + self.reference

    def get_selling_price(self):
        uhren = ["uhren", "watches"]
        discount = float(self.discount)

        def myround(x): return round(x, 1)  # rounding

        if self.category_object["group"].lower() in uhren:
            if discount >= 65:
                return myround(float(self.price) * 1.85)
            elif discount >= 55:
                return myround(float(self.price) * 1.80)
            elif discount >= 40:
                return myround(float(self.price) * 1.60)
            else:
                return myround(float(self.price) * 1.50)
        else:
            price = float(self.price)
            shipping_cost = 12
            return myround((price + shipping_cost) + (price * 0.30))

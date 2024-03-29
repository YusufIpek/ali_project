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
            "kind": "Kind",
            "herren und damen": "Unisex",
        }
        found = list(
            filter(lambda x: x["group_name"].lower() == "geschlecht", self.attributes)
        )

        if len(found) > 0:
            return (
                mapping[found[0]["value_name"].lower()]
                + self.category_object["group"].strip()
            )
        else:
            return "Unbekannt" + self.category_object["group"].strip()

    def get_title(self):
        # if self.brand_name.lower().strip() == 'guess':
        if self.reference in self.name:
            return self.name
        return self.name + " - " + self.reference

    def get_tags(self):
        tags = [self.id_product, "dropshipping"]
        if self.is_product_smartwatch():
            tags.append("smartwatch")
        return tags

    def is_product_smartwatch(self):
        found = list(
            filter(
                lambda x: x["group_name"].lower() == "produktart"
                and x["value_name"].lower() == "smartuhr",
                self.attributes,
            )
        )
        if len(found):
            return True

        # unfortunately under the smartwatch category there are also watches which are not smartwatches, thus keep the below code commented out
        # if self.category_object["category"].lower() == "smart uhren":
        #     return True

        return False

    def get_selling_price(self):
        uhren = ["uhren", "watches"]
        discount = float(self.discount)

        def myround(x):
            return round(x, 1)  # rounding

        def special_price_calc(item, discount, price):
            if price < 40 and discount < 70:
                return item.retail_price
            else:
                return price

        result = 0.0
        if self.category_object["group"].lower() in uhren:
            # price calculation for watches
            if discount >= 75:
                result = special_price_calc(
                    self, discount, myround(float(self.price) * 2.30)
                )
            elif discount >= 65:
                result = special_price_calc(
                    self, discount, myround(float(self.price) * 2.20)
                )
            elif discount >= 55:
                result = special_price_calc(
                    self, discount, myround(float(self.price) * 2.00)
                )
            elif discount >= 45:
                result = special_price_calc(
                    self, discount, myround(float(self.price) * 1.70)
                )
            elif discount >= 40:
                result = special_price_calc(
                    self, discount, myround(float(self.price) * 1.50)
                )
            else:
                result = myround(float(self.retail_price))
        else:
            # price calculation for jewelry
            price = float(self.price)
            shipping_cost = 12
            result = myround((price + shipping_cost) + (price * 0.30))

        if (
            self.category_object["name"].lower().strip() == "esprit"
            or self.category_object["name"].lower().strip() == "pierre cardin"
        ):
            result += 15
        else:
            result += 10

        return result

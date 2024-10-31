class Product:
    def __init__(self, href, img, name, converted_price, current_currency, **other_data):
        self.href = href
        self.img = img
        self.name = name
        self.converted_price = converted_price
        self.current_currency = current_currency
        self.other_data = other_data

    def to_dict(self):
        return {
            "href": self.href,
            "img": self.img,
            "name": self.name,
            "converted_price": self.converted_price,
            "current_currency": self.current_currency,
            "other_data": self.other_data
        }

    def __repr__(self):
        return (f"Product(name={self.name}, price={self.converted_price} {self.current_currency}, "
                f"other_data={self.other_data})")

def liviu_serialization(data):
    if isinstance(data, dict):
        return serialize_dict(data)
    elif isinstance(data, list):
        return serialize_list(data)
    elif hasattr(data, "__dict__"):
        return serialize_object(data)
    else:
        return serialize_value(data)

def serialize_dict(data):
    items = []
    for key, value in data.items():
        custom_key = to_custom_key(key)
        serialized_value = liviu_serialization(value)
        items.append(f"<{custom_key}>{serialized_value}</{custom_key}>")
    return ''.join(items)

def serialize_list(data):
    items = [f"<item>{liviu_serialization(item)}</item>" for item in data]
    return ''.join(items)

def serialize_object(obj):
    items = []
    for key, value in obj.__dict__.items():
        custom_key = to_custom_key(key)
        serialized_value = liviu_serialization(value)
        items.append(f"<{custom_key}>{serialized_value}</{custom_key}>")
    return ''.join(items)

def serialize_value(value):
    if isinstance(value, str):
        return value
    elif isinstance(value, (int, float)) and not isinstance(value, bool):
        return str(value)
    elif isinstance(value, bool):
        return 'true' if value else 'false'
    elif value is None:
        return ""
    else:
        raise ValueError(f"Unsupported type: {type(value)}")

def to_custom_key(key):
    custom_keys = {
        'name': 'Name',
        'converted_price': 'Price',
        'current_currency': 'Currency',
        'other_data': 'OtherData',
        'href': 'Href',
        'img': 'Img',
    }
    return custom_keys.get(key, key)  # Return the custom key or the original key if not found

# Example usage
product_data = {
    'href': 'https://xstore.md/laptopuri/gaming/lenovo-loq-15ahp9-15-6-ryzen-7-8845hs-16gb-ram-1tb-ssd-rtx4050',
    'img': 'https://xstore.md/images/product/thumbs/2024/03/Lenovo-LOQ-15AHP9-83DX006PRK--1-.jpg',
    'name': 'Lenovo LOQ 15AHP9',
    'converted_price': 1131.5263157894738,
    'current_currency': 'EUR',
    'other_data': {
        'price': 21499,
        'currency': 'lei',
        'Diagonală': '15.6inch',
        'Procesor': 'AMD Ryzen 7 8845HS',
        'Capacitatea RAM': '16 GB',
        'Unitate de stocare': '1 TB (SSD)',
        'Placă video': 'NVIDIA GeForce RTX 4050'
    }
}

serialized_product = liviu_serialization(product_data)
print(serialized_product)

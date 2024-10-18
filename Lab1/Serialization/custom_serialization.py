def liviu_serialization(product):
    # Create a list to hold the serialized lines
    serialized_lines = []

    # Main product attributes
    serialized_lines.append(f"Href: {product.href}")
    serialized_lines.append(f"Img: {product.img}")
    serialized_lines.append(f"Name: {product.name}")
    serialized_lines.append(f"Price: {product.converted_price:.2f}")
    serialized_lines.append(f"Currency: {product.current_currency}")
    
    # Other data
    serialized_lines.append("OtherData:")
    for key, value in product.other_data.items():
        serialized_lines.append(f"  {key}: {value}")
    
    return "\n".join(serialized_lines)

def liviu_deserialization(serialized_string: str):
    lines = serialized_string.strip().split('\n')
    
    # Create an empty dictionary to store the product data
    product_data = {}
    other_data = {}

    # Parse each line
    for line in lines:
        line = line.strip()
        if line.startswith("Href:"):
            product_data['href'] = line.split("Href:")[1].strip()
        elif line.startswith("Img:"):
            product_data['img'] = line.split("Img:")[1].strip()
        elif line.startswith("Name:"):
            product_data['name'] = line.split("Name:")[1].strip()
        elif line.startswith("Price:"):
            product_data['converted_price'] = float(line.split("Price:")[1].strip())
        elif line.startswith("Currency:"):
            product_data['current_currency'] = line.split("Currency:")[1].strip()
        elif line.startswith("OtherData:"):
            # Start capturing other data
            continue
        else:
            # Capture other data entries
            key, value = line.split(":", 1)
            other_data[key.strip()] = value.strip()

    # Add the other data to the main product data dictionary
    product_data['other_data'] = other_data

    return product_data
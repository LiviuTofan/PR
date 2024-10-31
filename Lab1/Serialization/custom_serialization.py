from Serialization.Product import Product

def liviu_serialization(data):
    if isinstance(data, Product):
        serialized_lines = []
        serialized_lines.append(f"Href: {data.href}")
        serialized_lines.append(f"Img: {data.img}")
        serialized_lines.append(f"Name: {data.name}")
        serialized_lines.append(f"Price: {data.converted_price:.2f}")
        serialized_lines.append(f"Currency: {data.current_currency}")
        
        serialized_lines.append("OtherData:")
        for key, value in data.other_data.items():
            serialized_lines.append(f"  {key}: {value}")

        return "\n".join(serialized_lines)
    
    elif isinstance(data, list):
        return "\n".join([liviu_serialization(item) for item in data])
    
    elif isinstance(data, dict):
        return "\n".join([f"{key}: {value}" for key, value in data.items()])
    
    elif isinstance(data, str):
        return f'String: {data}'
    
    elif isinstance(data, (int, float)):
        return f'Number: {data}'
    
    elif isinstance(data, bool):
        return f'Boolean: {data}'
    
    else:
        return 'Unsupported data type'

def liviu_deserialization(serialized_string: str):
    lines = serialized_string.strip().split('\n')
    
    product_data = {}
    other_data = {}

    current_section = None

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
            current_section = "OtherData"
            continue  # Skip the "OtherData:" line
        elif current_section == "OtherData":
            key, value = line.split(":", 1)
            other_data[key.strip()] = value.strip()
        else:
            # Handle unexpected lines
            key, value = line.split(":", 1)
            product_data[key.strip()] = value.strip()

    product_data['other_data'] = other_data

    return product_data

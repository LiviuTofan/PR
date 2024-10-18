def custom_xml_serialize(obj):
    if isinstance(obj, dict):
        items = [f"<{k}>{custom_xml_serialize(v)}</{k}>" for k, v in obj.items()]
        return ''.join(items)
    elif isinstance(obj, list):
        items = [f"<item>{custom_xml_serialize(item)}</item>" for item in obj]
        return ''.join(items)
    elif isinstance(obj, str):
        return f"{obj}"
    elif isinstance(obj, (int, float)) and not isinstance(obj, bool):
        return str(obj)
    elif isinstance(obj, bool):
        return 'true' if obj else 'false'
    elif obj is None:
        return ""
    else:
        obj_dict = obj.__dict__
        serialized_data = custom_xml_serialize(obj_dict)
        return f"<Product>{serialized_data}</Product>"


def custom_xml_deserialize(xml_string: str):
    parsed_data = decode_dict(xml_string)
    return parsed_data

def decode_dict(content: str):
    items = {}

    while content:
        start = content.find('<')
        end = content.find('>', start)
        if start == -1 or end == -1:
            break

        key = content[start + 1:end]
        value_start = end + 1
        value_end = content.find(f'</{key}>', value_start)

        if value_end == -1: 
            break

        value_xml = content[value_start:value_end].strip()

        if has_nested_tags(value_xml):
            # Recursively decode if there are nested tags
            items[key] = decode_dict(value_xml)
        else:
            items[key] = decode_value(value_xml)

        # Move to the next key
        content = content[value_end + len(f'</{key}>'):].strip()

    return items

def has_nested_tags(content: str):
    return '<' in content and '>' in content and content.count('<') > 1

def decode_value(value: str):
    value = value.strip()
    if value.lower() == 'true':
        return True
    elif value.lower() == 'false':
        return False
    try:
        return int(value)
    except ValueError:
        try:
            return float(value)
        except ValueError:
            return
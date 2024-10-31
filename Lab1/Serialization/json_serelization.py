import re

def custom_json_serialize(obj):
    if isinstance(obj, dict):
        items = [f'"{k}": {custom_json_serialize(v)}' for k, v in obj.items()]
        return '{' + ', '.join(items) + '}'
    elif isinstance(obj, list):
        items = [custom_json_serialize(item) for item in obj]
        return '[' + ', '.join(items) + ']'
    elif isinstance(obj, str):
        return f'"{obj}"'
    elif isinstance(obj, (int, float)) and not isinstance(obj, bool):
        return str(obj)
    elif isinstance(obj, bool):
        return 'true' if obj else 'false'
    elif obj is None:
        return 'null'
    else:
        obj_dict = obj.__dict__
        return custom_json_serialize(obj_dict)
    

def custom_json_deserialize(data):
    if data == "null":
        return None
    elif data == "true":
        return True
    elif data == "false":
        return False
    elif data.startswith('"') and data.endswith('"'):
        return data[1:-1]
    elif data.startswith('[') and data.endswith(']'):
        return deserialize_list(data)
    elif data.startswith('{') and data.endswith('}'):
        return deserialize_dict(data)
    elif is_number(data):
        return float(data) if '.' in data else int(data)
    else:
        return data

def deserialize_list(data):
    # remove brackets and split by commas
    data = data[1:-1].strip()
    if not data:
        return []
    items = split_by_comma(data)
    return [custom_json_deserialize(item.strip()) for item in items]

def deserialize_dict(data):
    # remove curly braces and split by commas
    data = data[1:-1].strip()
    if not data:
        return {}
    items = split_by_comma(data)
    result = {}
    for item in items:
        key, value = item.split(':', 1)
        key = custom_json_deserialize(key.strip())
        value = custom_json_deserialize(value.strip())
        result[key] = value
    return result

def split_by_comma(data):
    # split the string by commas, ignoring commas inside nested structures
    result = []
    bracket_level = 0
    current_item = []
    
    for char in data:
        if char == ',' and bracket_level == 0:
            result.append(''.join(current_item).strip())
            current_item = []
        else:
            current_item.append(char)
            if char == '{' or char == '[':
                bracket_level += 1
            elif char == '}' or char == ']':
                bracket_level -= 1
    
    result.append(''.join(current_item).strip())
    return result

def is_number(data):
    try:
        float(data)
        return True
    except ValueError:
        return False

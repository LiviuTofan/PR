import unittest
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
    elif isinstance(obj, (int, float)) and not isinstance(obj, bool):  # Prevent booleans from being treated as numbers
        return str(obj)
    elif isinstance(obj, bool):
        return 'true' if obj else 'false'
    elif obj is None:
        return 'null'
    else:
        obj_dict = obj.__dict__
        return custom_json_serialize(obj_dict)



def custom_json_deserialize(data_str):
    data_str = re.sub(r'\bnull\b', 'None', data_str)
    data_str = re.sub(r'\btrue\b', 'True', data_str)
    data_str = re.sub(r'\bfalse\b', 'False', data_str)
    return eval(data_str)


class TestCustomJSONSerialization(unittest.TestCase):
    
    def test_serialize_dictionary(self):
        data = {"name": "John", "age": 30}
        expected = '{"name": "John", "age": 30}'
        self.assertEqual(custom_json_serialize(data), expected)

    def test_serialize_list(self):
        data = [1, 2, 3, "apple", True, None]
        expected = '[1, 2, 3, "apple", true, null]'
        self.assertEqual(custom_json_serialize(data), expected)

    def test_serialize_string(self):
        data = "Hello, World!"
        expected = '"Hello, World!"'
        self.assertEqual(custom_json_serialize(data), expected)

    def test_serialize_integer(self):
        data = 42
        expected = '42'
        self.assertEqual(custom_json_serialize(data), expected)

    def test_serialize_float(self):
        data = 3.14159
        expected = '3.14159'
        self.assertEqual(custom_json_serialize(data), expected)

    def test_serialize_boolean(self):
        data = True
        expected = 'true'
        self.assertEqual(custom_json_serialize(data), expected)

    def test_serialize_none(self):
        data = None
        expected = 'null'
        self.assertEqual(custom_json_serialize(data), expected)
    
    def test_deserialize_dictionary(self):
        data_str = '{"name": "John", "age": 30}'
        expected = {'name': 'John', 'age': 30}
        self.assertEqual(custom_json_deserialize(data_str), expected)
    
    def test_deserialize_list(self):
        data_str = '[1, 2, 3, "apple", True, null]'
        expected = [1, 2, 3, 'apple', True, None]
        self.assertEqual(custom_json_deserialize(data_str), expected)

    def test_deserialize_string(self):
        data_str = '"Hello, World!"'
        expected = 'Hello, World!'
        self.assertEqual(custom_json_deserialize(data_str), expected)

    def test_deserialize_integer(self):
        data_str = '42'
        expected = 42
        self.assertEqual(custom_json_deserialize(data_str), expected)

    def test_deserialize_float(self):
        data_str = '3.14159'
        expected = 3.14159
        self.assertEqual(custom_json_deserialize(data_str), expected)

    def test_deserialize_boolean(self):
        data_str = 'true'
        expected = True
        self.assertEqual(custom_json_deserialize(data_str), expected)

    def test_deserialize_none(self):
        data_str = 'null'
        expected = None
        self.assertEqual(custom_json_deserialize(data_str), expected)

if __name__ == '__main__':
    unittest.main()

import json

def get_product(cursor, product_id, columns):
    cursor.execute('SELECT * FROM product WHERE id = ?', (product_id,))
    product_row = cursor.fetchone()
    if product_row is None:
        return None

    product_data = {
        "href": product_row[1],
        "img": product_row[2],
        "name": product_row[3],
        "converted_price": product_row[4],
        "current_currency": product_row[5]
    }

    cursor.execute('SELECT * FROM other_data WHERE product_id = ?', (product_id,))
    other_data_rows = cursor.fetchall()
    product_data['other_data'] = {}

    i=2
    for column in columns:
        product_data['other_data'][column] = other_data_rows[0][i]
        i+=1

    return json.dumps(product_data)

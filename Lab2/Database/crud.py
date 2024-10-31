def get_product(cursor, product_id):
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
    other_data_row = cursor.fetchone()

    if other_data_row:
        product_data['other_data'] = {}
        for i in range(2, len(other_data_row)):
            product_data['other_data'][other_data_row[i]] = other_data_row[i]
    else:
        product_data['other_data'] = {}
    
    return product_data

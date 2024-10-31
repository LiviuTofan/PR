def parse_main_page(content):
    products = {}
    anchor_tags = content.find_all('a', class_='xcateg')
    for ancho_tag in anchor_tags:
        href = ancho_tag.get('href')
        span = ancho_tag.find('span')
        category = span.text
        products[category] = href

    return products
from product_scraping import product_scraping

# Scrape all products from a category page and call the function to scrape each product apart
def category_scraping(content):
    products = []
    div = content.find('div', class_='category-prods xlists')
    anchor_tags = div.find_all('a', class_='img-wrap')
    for anchor_tag in anchor_tags:
        product = {}
        product_href = anchor_tag.get('href')
        img = anchor_tag.find('img').get('src')
        product['href'] = product_href
        product['img'] = img

        product = product_scraping(product_href, product)
        products.append(product)

    return products
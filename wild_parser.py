import requests
from bs4 import BeautifulSoup

HOST = 'https://www.wildberries.ru/catalog/'
SYFFIX = '/detail.aspx?targetUrl=XS'
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.37',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
}

prodact_items = ['10116961', '35416262', '59894220']


# prodact_items = ['10116961']

def get_page(url, params=''):
    s = requests.Session()
    response = s.get(url=url, headers=headers, params=params)
    return response.text


def strToDigit(str):
    return int(''.join(c for c in str if c.isdigit() == True))


def save_in_file(data):
    with open("index.html", "w", encoding="utf-8") as file:
        file.write(data)


def get_content(html, print_result=False):
    '''
    :param html:
    :param print_result: bool - for print result
    :return: dict of params product
    '''
    # with open('out.txt','w',encoding="utf-8") as f:
    #     f.write(html)
    soup = BeautifulSoup(html, 'html.parser')

    # check of exsist of product
    tovara_net = soup.find('div', class_='same-part-kt__sold-out-product hide-desktop')
    if not tovara_net:  # if product is exsist, find next data
        name_item = soup.find('h1', class_='same-part-kt__header')
        if name_item:
            name_item = name_item.get_text().split(' ')[0]
        # product description
        opisanie_item = soup.find('h1', class_='same-part-kt__header').find_all('span')[1].get_text()
        price = soup.find('span', class_='price-block__commission-current-price')
        if price:
            price = price.get_text().replace(' ', '')
            price = strToDigit(price)
        else:
            price = soup.find('span', class_='price-block__final-price')

            if price:
                price = price.get_text().replace(' ', '')
                price = strToDigit(price)

        price_old = soup.find('del', class_='price-block__old-price j-final-saving')

        if price_old:
            price_old = price_old.get_text()
            price_old = strToDigit(price_old)
        if print_result:
            print(f'name= {name_item} \nOpisanie= {opisanie_item}\nЦена без скидок= {price_old}\nЦена со скидкой магазина= '
              f'{price}\n')
        item = {
            'name_item': f'{name_item}',
            'description': f'{opisanie_item}',
            'price_old': f'{price_old}',
            'price': f'{price}',
        }
        return item
    else:
        print('Товара нет')
        return 0


def main():
    for item in prodact_items:
        url = HOST + item + SYFFIX
        page = get_page(url=url)
        print(get_content(page))


if __name__ == '__main__':
    main()

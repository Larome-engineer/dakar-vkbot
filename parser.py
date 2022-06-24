import requests
from bs4 import BeautifulSoup


URL = 'https://www.farpost.ru/user/DaKar41/auto/wheel/tire/'
HOST = 'https://www.farpost.ru'
HEADERS = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.125 Safari/537.36',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'
}


def get_pages_count(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all("tr", class_="page-splitter")

    pa = []
    for item in items:
        pa.append({
            'title': item.find("th").get_text(),
        })

    print(pa)


def get_html(url, params=None):
    r = requests.get(url, headers=HEADERS, params=params)
    return r


def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all("tr", class_="bull-item bull-item_inline -exact bull-item bull-item_inline")

    wheels = []
    for item in items:
        wheels.append({
            'title': item.find("a", class_="bulletinLink bull-item__self-link auto-shy").get_text(),
            'link': HOST + item.find("a", class_="bulletinLink bull-item__self-link auto-shy").get('href'),
            'price': item.find("span", class_="price-block__price").get_text()
        })

    print(wheels)


def parse():
    html = get_html(URL)
    if html.status_code == 200:
        print(get_pages_count(html.text))
        get_content(html.text)
    else:
        print('Error')


parse()

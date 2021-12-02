import requests
from bs4 import BeautifulSoup
from pprint import pprint

response = requests.get('https://habr.com/ru/all/')
response.raise_for_status()

KEYWORDS = ['дизайн', 'фото', 'web', 'python']
dword = []
result = []

soup = BeautifulSoup(response.text, features='html.parser')
articles = soup.find_all('article')


def get_stream(streams_list):
    try:
        for article in articles:
            dates = article.find('span', class_="tm-article-snippet__datetime-published")
            headers = article.find('h2', class_="tm-article-snippet__title tm-article-snippet__title_h2")
            links = article.find('a', class_="tm-article-snippet__title-link")
            text_v2 = article.find('div', class_="article-formatted-body article-formatted-body_version-2")
            text_v1 = article.find('div', class_="article-formatted-body article-formatted-body_version-1")

            if text_v2 is None:
                streams_list.append(
                    {'date': dates.text, 'header': headers.text, 'link': links['href'], 'text': text_v1.text.strip()}
                )
            elif text_v1 is None:
                streams_list.append(
                    {'date': dates.text, 'header': headers.text, 'link': links['href'], 'text': text_v2.text.strip()}
                )
    except AttributeError:
        return 'Возможно конструкция страницы изменилась'


def get_result(dword_list, result_list):
    get_stream(dword_list)
    for dword_title_list in dword:
        for k_word in KEYWORDS:
            if k_word in dword_title_list.get('text'):
                result_list.append(
                    f'{dword_title_list["date"]} - {dword_title_list["header"]} - https://habr.com{dword_title_list["link"]}')


get_result(dword, result)

if not result:
    print('---> Список пуст <---')
else:
    print(set(result))

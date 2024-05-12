from pprint import pprint
from bs4 import BeautifulSoup
import requests
import re
from json import dump

DOMEAN = "https://avtovesti.com/"

response = requests.get(DOMEAN)
soup = BeautifulSoup(response.text, "html.parser")

# Поиск ссылок на новости
sp = soup.find_all("span", itemprop="headline")
acl = []
for a in sp:
    href = a.find_all("a")

    acl.append(href)

result_all = []
links = []
pattern = re.compile(r'href="([^"]+)"')
for a in acl:
    a_html = str(a)
    match = pattern.search(a_html)
    if match:
        links.append(match.group(1))

#all_text = []
for link in links:
    result = {}
    response= requests.get(link)
    soup = BeautifulSoup(response.text, "html.parser")
    # Заголовки
    news_title = soup.find_all("h1", class_="entry-title")
    for new in news_title:
        result["Заголовок"] = new.text
    # Дата
    news_dates = soup.find_all("time", itemprop="datePublished")
    for data in news_dates:
        result["Дата публикации"] = data.text
    # Начало статьи
    news_anatations = soup.find("div", id="bsf_rt_marker")
    text = []
    for anat in news_anatations:
        text.append(anat.text)
    result["Анатация"] = text[0]
    # Весь текст статьи
    news_text = soup.find_all("div", id="bsf_rt_marker")
    all_text = []
    for text in news_text:
        all_text.append(text.text)

    result["Читать далее"] = all_text
    result["Источник"] = link

    result_all.append(result)

pprint(result_all)

with open('all_news.json', mode='w', encoding='utf-8') as f:
    dump(result_all, f, ensure_ascii=False)
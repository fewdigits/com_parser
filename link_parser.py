import requests
from bs4 import BeautifulSoup


def get_html(url):
    headers = {'User-Agent': 'My User Agent 1.0'}
    r = requests.get(url, headers=headers)
    return r.text


def get_links(html):
    href = []
    header = []
    soup = BeautifulSoup(html, 'lxml')
    divs = soup.find_all('div', class_='bl2 blpad bla')
    for div in divs:
        links = div.find_all('a')
        for link in links:
            if link['href'].startswith('http') or link['href'].endswith('/'):
                continue
            href.append(link['href'])
            header.append(link.text.strip())

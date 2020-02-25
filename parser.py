import requests
from bs4 import BeautifulSoup
import csv


def get_html(url):
    headers = {'User-Agent': 'My User Agent 1.0'}
    r = requests.get(url, headers=headers)
    return r.text


def get_total_pages(html):
    soup = BeautifulSoup(html, 'lxml')
    divs = soup.find('div', class_='link_bar')
    span = soup.find('span', class_='pagelinklast')
    pages = 0
    if span:
        pages = span.find('a').text.strip()
        return int(pages)
    elif divs:
        links = divs.find_all('a')
        for link in links:
            if link['href'].startswith('?page'):
                pages += 1
            else:
                continue
        return pages + 2
    else:
        return 0


def write_csv(filename, data):
    with open(f'csv/{filename}.csv', 'a') as f:
        writer = csv.writer(f, delimiter=',')
        writer.writerow((data['title'], data['email']))


def get_page_data(html, filename):
    soup = BeautifulSoup(html, 'lxml')
    divs = soup.find_all('div', class_='anryblimg2')
    for div in divs:
        title = div.find('h2').text.strip()
        links = div.find_all('a')
        for link in links:
            if link['href'].startswith('mailto:'):
                email = link.text.strip()
            else:
                email = 'missing'
        data = {'title': title, 'email': email}
        if email != 'missing':
            write_csv(filename, data)
        else:
            continue


def get_data(url, filename):
    base_url = 'https://cheb.ru'
    page_part = '?page='
    total_pages = get_total_pages(get_html(base_url + url))
    if total_pages > 0:
        for i in range(1, total_pages):
            url_gen = base_url + url + page_part + str(i)
            html = get_html(url_gen)
            get_page_data(html, filename)
    else:
        html = get_html(base_url)
        get_page_data(html, filename)


def main():
    href = []
    header = []
    soup = BeautifulSoup(get_html('https://cheb.ru/spravka/'), 'lxml')
    divs = soup.find_all('div', class_='bl2 blpad bla')
    for div in divs:
        links = div.find_all('a')
        for link in links:
            if link['href'].startswith('http') or link['href'].endswith('/'):
                continue
            href.append(link['href'])
            header.append(link.text.strip())

    info = list(zip(href, header))

    for item in info:
        get_data(item[0], item[1])


if __name__ == '__main__':
    main()

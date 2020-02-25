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
    pages = divs.find_all('span', class_='pagelink')
    return len(pages) + 1


def write_csv(data):
    with open('data.csv', 'a') as f:
        writer = csv.writer(f, delimiter=',')
        writer.writerow((data['title'], data['email']))


def get_page_data(html):
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
            write_csv(data)
        else:
            continue


def main():
    base_url = 'https://cheb.ru/unitar.htm'
    page_part = '?page='
    total_pages = get_total_pages(get_html(base_url))

    for i in range(1, total_pages):
        url = base_url + page_part + str(i)
        html = get_html(url)
        get_page_data(html)


if __name__ == '__main__':
    main()

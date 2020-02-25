import requests
from bs4 import BeautifulSoup
import csv


def get_html(url):
    headers = {'User-Agent': 'My User Agent 1.0'}
    r = requests.get(url, headers=headers)
    return r.text


def write_csv(data):
    with open('data.csv', 'a') as f:
        writer = csv.writer(f)
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
                email = ''
        data = {'title': title, 'email': email}
        # print(data)
        write_csv(data)


def main():
    url = 'https://cheb.ru/unitar.htm'
    html = get_html(url)
    get_page_data(html)


if __name__ == '__main__':
    main()

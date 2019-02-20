import requests
import json
import re
from requests.exceptions import RequestException
from urllib.parse import urlencode
from bs4 import BeautifulSoup


def get_page_index(offset, keyword):
    data = {
        'aid': 24,
        'app_name': 'web_search',
        'offset': 0,
        'format': 'json',
        'keyword': keyword,
        'autoload': 'true',
        'count': 20,
        'en_qc': 1,
        'cur_tab': 1,
        'from': 'search_tab',
        'pd': 'synthesis'
    }
    url = 'https://www.toutiao.com/api/search/content/?' + urlencode(data)
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        print('请求索引页出错')
        return None


def parse_page_index(html):
    data = json.loads(html)
    if data and 'data' in data.keys():
        for item in data.get('data'):
            yield item.get('article_url')


def get_page_detail(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        print('请求详情页出错', url)
        return None


def parse_page_detail(html):
    soup = BeautifulSoup(html, 'html.parser')
    # title = soup.select('title')[0].get_text()
    # print(title)
    images_pattern = re.compile('content(.*?);', re.S)
    result = re.search(images_pattern, html)
    if result:
        print(result.group(1))


def main():
    html = get_page_index(0, '街拍')
    for url in parse_page_index(html):
        # print(url)
        html = get_page_detail(url)
        if html:
            parse_page_detail(html)


if __name__ == '__main__':
    main()

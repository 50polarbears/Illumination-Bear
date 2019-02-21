import requests
from bs4 import BeautifulSoup
from bs4.dammit import EncodingDetector
from collections import Counter

def get_politifact_articles():
    url = 'https://www.politifact.com/truth-o-meter/article/'

    resp = requests.get(url)
    # http_encoding = resp.encoding if 'charset' in resp.headers.get('content-type', '').lower() else None
    # html_encoding = EncodingDetector.find_declared_encoding(resp.content, is_html=True)
    # encoding = html_encoding or http_encoding
    soup = BeautifulSoup(resp.content, 'lxml')#, from_encoding=encoding)

    stories = soup.find_all('h3', class_="story__title")
    story_links = ['https://politifact.com' + story.find('a')['href'] for story in stories]
    return story_links[::-1]

def scrape_politifact_article(story_url):
    resp = requests.get(story_url)
    http_encoding = resp.encoding if 'charset' in resp.headers.get('content-type', '').lower() else None
    html_encoding = EncodingDetector.find_declared_encoding(resp.content, is_html=True)
    encoding = html_encoding or http_encoding
    soup = BeautifulSoup(resp.content, 'lxml', from_encoding=encoding)
    return soup.find("div", "article__text").get_text()

if __name__ == '__main__':
    print(get_politifact_articles()[0])
    print(scrape_politifact_article('https://www.politifact.com/truth-o-meter/article/2019/feb/19/what-2019-oscar-movies-get-right-wrong/'))

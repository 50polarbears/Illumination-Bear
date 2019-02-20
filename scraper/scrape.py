from scraper_core import *

def scrape(testing=False):
    if testing:
        stories = [get_politifact_articles()[0]]
    else:
        stories = get_politifact_articles()
    for url in stories:
        yield scrape_politifact_article(url)

if __name__ == '__main__':
    [x] = list(scrape(testing=True))
    print(x)

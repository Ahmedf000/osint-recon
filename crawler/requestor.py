import requests
from bs4 import BeautifulSoup

def crawler(url):
    hrefs = []
    webpage = requests.get(url)
    soup = BeautifulSoup(webpage.content, 'html.parser')
    href = soup.find_all('a')
    try:
        for h in href:
            hrefs.append(h.get('href'))
        return hrefs
    except AttributeError:
        return f"Error occured while crawling {url}"



def further_crawler(href):
    pass

#further crawler within the crawler function found links
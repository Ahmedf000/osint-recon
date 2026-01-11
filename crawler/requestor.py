import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from typing import List, Set, Optional
from crawler.proxy import *


def crawler(url: str, proxy_manager=None, depth: int = 1, max_depth: int = 2, visited: Set[str] = None) -> List[str]:

    if visited is None:
        visited = set()

    if url in visited:
        return []

    if depth > max_depth:
        return []

    visited.add(url)

    hrefs = []

    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

        if proxy_manager and proxy_manager.get_working_count() > 0:
            proxy = proxy_manager.get_next_proxy()
            proxies = proxy_manager.get_proxy_dict(proxy)

            try:
                webpage = requests.get(
                    url,
                    proxies=proxies,
                    headers=headers,
                    timeout=10
                )

            except Exception as e:
                print(f"[!] Proxy failed for {url}, trying without proxy")
                proxy_manager.mark_proxy_failed(proxy)
                webpage = requests.get(url, headers=headers, timeout=10)


        else:
            webpage = requests.get(url, headers=headers, timeout=10)

        soup = BeautifulSoup(webpage.content, 'html.parser')
        links = soup.find_all('a')

        for link in links:
            href = link.get('href')

            if not href:
                continue

            absolute_url = urljoin(url, href)

            if not absolute_url.startswith(('http://', 'https://')):
                continue

            if '#' in absolute_url:
                absolute_url = absolute_url.split('#')[0]

            if not absolute_url or absolute_url == url:
                continue

            if absolute_url not in visited:
                hrefs.append(absolute_url)

        hrefs = list(set(hrefs))

        print(f"[*] Crawled {url}: found {len(hrefs)} links (depth {depth}/{max_depth})")

        if depth < max_depth:
            for found_url in hrefs[:5]:
                if found_url not in visited:
                    sub_hrefs = crawler(found_url, proxy_manager, depth + 1, max_depth, visited)
                    hrefs.extend(sub_hrefs)

        return hrefs

    except requests.exceptions.Timeout:
        print(f"[!] Timeout crawling {url}")
        return []
    except requests.exceptions.RequestException as e:
        print(f"[!] Error crawling {url}: {e}")
        return []
    except Exception as e:
        print(f"[!] Unexpected error crawling {url}: {e}")
        return []


def simple_crawler(url: str) -> List[str]:
    return crawler(url, max_depth=1)
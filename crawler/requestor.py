import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from typing import List, Set, Optional
import time


def crawler(
        url: str,
        proxy_manager=None,
        depth: int = 1,
        max_depth: int = 2,
        visited: Optional[Set[str]] = None,
        robot_checker=None,
        respect_robots: bool = True
) -> List[str]:

    if visited is None:
        visited = set()

    if url in visited:
        return []

    if depth > max_depth:
        return []

    if respect_robots and robot_checker:
        if not robot_checker.can_crawl(url):
            print(f"[!] Blocked by robots.txt: {url}")
            return []

        delay = robot_checker.get_crawl_delay(url)
        if delay > 0:
            print(f"[*] Respecting crawl delay: {delay}s")
            time.sleep(delay)

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

        if webpage.status_code != 200:
            print(f"[!] HTTP {webpage.status_code} for {url}")
            return []

        soup = BeautifulSoup(webpage.content, 'html.parser')
        links = soup.find_all('a')

        base_domain = urlparse(url).netloc

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
            links_to_crawl = hrefs[:5]

            for found_url in links_to_crawl:
                if found_url not in visited:
                    sub_hrefs = crawler(
                        found_url,
                        proxy_manager,
                        depth + 1,
                        max_depth,
                        visited,
                        robot_checker,
                        respect_robots
                    )
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


def simple_crawler(url: str, proxy_manager=None) -> List[str]:
    return crawler(url, proxy_manager=proxy_manager, max_depth=1)


def crawl_with_robots(url: str, proxy_manager=None, robot_checker=None, max_depth: int = 1) -> List[str]:
    return crawler(
        url,
        proxy_manager=proxy_manager,
        max_depth=max_depth,
        robot_checker=robot_checker,
        respect_robots=True
    )
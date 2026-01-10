import requests
import random
import time
from typing import List, Optional

class ProxyManager:
    def __init__(self):
        self.proxies = []
        self.failed_proxies = set()
        self.current_index = 0



    def load_proxies_from_list(self, proxies_list: List[str]):
        print(f"Loading {len(proxies_list)} proxies.....")
        self.proxies = [p for p in proxies_list if p not in self.failed_proxies]
        print(f"Loaded {len(self.proxies)} proxies.")



    def load_proxies_from_file(self, filename: str):
        try:
            with open(filename, 'r') as f:
                proxies_list = [line.strip() for line in f if line.strip()]

                formatted = []
                for p in proxies_list:
                    if not p.startswith("http"):
                        p = f"http://{p}"
                    formatted.append(p)

            self.load_proxies_from_list(formatted)
        except FileNotFoundError:
            print(f"[!] File {filename} not found.]")
        except Exception as e:
            print(f"[!] {e}.")




    def fetch_free_proxy(self):
        print(f"[*] Fetching Free proxies from API....")
        try:
            response = requests.get(
                'https://api.proxyscrape.com/v2/',
                params={
                    'request': 'displayproxies',
                    'protocol': 'http',
                    'timeout': 10000,
                    'country': 'all',
                    'ssl': 'all',
                    'anonymity': 'all',
                },
                timeout=10,
            )

            if response.status_code == 200:
                proxy_list = response.text.strip().split('\n')
                formatted = [f"http://{p.strip()}" for p in proxy_list if p.strip()]
                self.load_proxies_from_list(formatted)
                return True
            else:
                print(f"[!] failed to fetch proxies from API: {response.status_code}")
                return False




    def test_proxies(self, proxy:str, timeout:int=5) -> bool:
        try:
            test_url = 'http://httpbin.org/ip'
            proxies = {
                'http': proxy,
                'https': proxy
            }
            response = requests.get(
                test_url,
                proxies=proxies,
                timeout=timeout
            )
            return response.status_code == 200
        except:
            return False



    def test_all_proxies(self, max_test:int=50):
        if not self.proxies:
            print("[!] No proxies to test.")
            return

        test_count = min(len(self.proxies), max_test)
        print(f"[*] Testing {test_count} proxies (this may take a minute).")

        working = []
        for i, proxy in enumerate(self.proxies[:test_count], 1):
            print(f"[*] Testing proxy {i}/{test_count}...", end='\r')
            if self.test_proxies(proxy):
                working.append(proxy)

        self.proxies = working
        print(f"\n[+] {len(self.proxies)} working proxies found!")

        if len(self.proxies) == 0:
            print("[!] WARNING: No working proxies found!")



    def get_next_proxy(self, strategy: str = 'rotate') -> Optional[str]:
        if not self.proxies:
            return None

        if strategy == 'rotate':
            proxy = self.proxies[self.current_index]
            self.current_index = (self.current_index + 1) % len(self.proxies)
            return proxy
        elif strategy == 'random':
            return random.choice(self.proxies)
        else:
            return self.proxies[0]


    def get_proxy_dict(self, proxy: str) -> dict:
        return {
            'http': proxy,
            'https': proxy
        }


    def get_working_count(self) -> int:
        return len(self.proxies)



def make_request_with_proxy(url: str, proxy_manager: ProxyManager, max_retries: int = 3):
    for attempt in range(max_retries):
        proxy = proxy_manager.get_next_proxy()

    if not proxy:
        try:
            return requests.get(url, timeout=10)
        except Exception as e:
            print(f"[!] Request failed without proxy: {e}")
            return None

    try:
        proxies = proxy_manager.get_proxy_dict(proxy)
        response = requests.get(url, proxies=proxies, timeout=10)
        return response

    except Exception as e:
        print(f"[!] Proxy {proxy} failed: {e}")
        proxy_manager.mark_proxy_failed(proxy)

        if attempt < max_retries - 1:
            print(f"[*] Retrying with different proxy... ({attempt + 2}/{max_retries})")

    print("[!] All proxy attempts failed")
    return None


























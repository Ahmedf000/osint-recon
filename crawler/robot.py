from urllib.robotparser import RobotFileParser
from urllib.parse import urlparse
from typing import Dict


class RobotChecker:
    def __init__(self):
        self.parsers: Dict[str, RobotFileParser] = {}
        self.user_agent = "OSINT-Recon-Bot"

    def can_crawl(self, url: str) -> bool:
        try:
            parsed = urlparse(url)
            domain = f"{parsed.scheme}://{parsed.netloc}"

            if domain not in self.parsers:
                self._load_robots(domain)

            parser = self.parsers.get(domain)

            if parser is None:
                return True

            return parser.can_fetch(self.user_agent, url)

        except Exception as e:
            print(f"[!] Error checking robots.txt: {e}")
            return True

    def get_crawl_delay(self, url: str) -> float:
        try:
            parsed = urlparse(url)
            domain = f"{parsed.scheme}://{parsed.netloc}"

            if domain not in self.parsers:
                self._load_robots(domain)

            parser = self.parsers.get(domain)

            if parser is None:
                return 0.0

            delay = parser.crawl_delay(self.user_agent)
            return delay if delay is not None else 0.0

        except:
            return 0.0

    def _load_robots(self, domain: str):
        try:
            robots_url = f"{domain}/robots.txt"
            parser = RobotFileParser()
            parser.set_url(robots_url)
            parser.read()
            self.parsers[domain] = parser
            print(f"[*] Loaded robots.txt for {domain}")
        except Exception as e:
            print(f"[!] Could not load robots.txt for {domain}: {e}")
            self.parsers[domain] = None
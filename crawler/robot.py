import os
import requests
from dotenv import load_dotenv
import sys

SITEMAP = {
        'sitemap_xml': ("robot.txt","filetype:xml site:{target} inurl:sitemap")
}

load_dotenv()

API_KEY = os.getenv("GOOGLE_API_KEY")
CX = os.getenv("GOOGLE_CX")

if not API_KEY or not CX:
    print("[!] Error: API credentials not found!")
    print("[!] Make sure .env file exists with GOOGLE_API_KEY and GOOGLE_CX")
    sys.exit(1)

def robot_auth():
    template = []
    for category in SITEMAP:
        for name, templates in SITEMAP[category]:
            template.append((templates))

    for iden, temp in template:
        if iden == 'robots.txt':
            continue
        try:
            filetype, site, url = temp
            template_dork = template.format(target=site)
            url = "https://www.googleapis.com/customsearch/v1"
            params = {
                'key': API_KEY,
                'cx': CX,
                'q': template_dork,
            }

            try:
                links = []
                request = requests.get(url, params=params)
                request.raise_for_status()

                response = request.json()
                links = response['items']
                for link in links[0]:
                    robot_response = requests.get(link['link'])
                return robot_response

            except requests.exceptions.RequestException as e:
                print(e)
            except Exception as e:
                print(f"[!] Error: {e}")
            except requests.exceptions.HTTPError as e:
                print(f"[!] Error for HTTP requets: {e}")

        except Exception as e:
            print(f"[!] Error: {e}")






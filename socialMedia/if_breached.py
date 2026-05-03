import requests
import json
from dotenv import load_dotenv
import sys
import os
from color.color import Colors

load_dotenv()

IF_BREACHED_API = os.getenv('BREACH_API')

if not load_dotenv():
    print("[!] Error: API key not found.")
    print("[!] Make sure you have your API key from https://hunting.abuse.ch/")
    sys.exit(1)


def additional_ip(ip_address):
    try:
        url = f'http://ip-api.com/json/{ip_address}'
        geo_request = requests.get(url, timeout=3)

        if geo_request.status_code == 200:
            data = geo_request.json()

            if data.get('status') == 'success':
                geo_data = {
                    'city': data.get('city', 'N/A'),
                    'region': data.get('regionName', 'N/A'),
                    'country': data.get('country', 'N/A'),
                    'isp': data.get('isp', 'N/A'),
                    'org': data.get('org', 'N/A'),
                    'lat': data.get('lat', 'N/A'),
                    'lon': data.get('lon', 'N/A'),
                    'timezone': data.get('timezone', 'N/A')
                }
                return geo_data
            else:
                return {'error': f"Geolocation failed: {data.get('message', 'Unknown error')}"}
        else:
            return {'error': f"HTTP {geo_request.status_code}"}

    except requests.RequestException as e:
        return {'error': f"Geolocation request failed: {str(e)}"}



def if_leaked(type_, query):

    url = "https://leak-lookup.com/api/search"
    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    try:
        res = requests.get(url,
                            key=IF_BREACHED_API,
                            type=type_,
                            query=f"{query}",
                            headers=HEADERS)
        if res.status_code == 200:
            data = json.loads(res.text)
            return data
        else:
            return {'error': f"Geolocation failed: {res.status_code}"}

    except requests.RequestException as e:
        return {'error': f"Geolocation request failed: {str(e)}"}



def email(query):
    query_email = if_leaked("email_address", query)
    print(Colors.green(query_email))

def ip(query):

    query_ip = if_leaked("ipaddress", query)
    if not query_ip:
        print(Colors.yellow("[!] Using ip-api.com instead"))
        query_additional_ip = additional_ip(query)
    if query_ip:
        print(Colors.green(query_ip))





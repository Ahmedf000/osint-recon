import requests
import sys
import argparse
import time
import re
import os
import json
from datetime import datetime
from dotenv import load_dotenv

from template import DORKS
from color.color import Colors
from crawler.proxy import ProxyManager
from crawler.requestor import crawler
from crawler.robot import RobotChecker

load_dotenv()

API_KEY = os.getenv('GOOGLE_API_KEY')
CX = os.getenv('GOOGLE_CX')

if not API_KEY or not CX:
    print("[!] Error: API credentials not found!")
    print("[!] Make sure .env file exists with GOOGLE_API_KEY and GOOGLE_CX")
    sys.exit(1)


def show_banner():
    banner = r"""

                                                              ..                                                         
                                                             .+#:       .-=-.                                            
                                                             -%==.   .-*+:.-++:                                          
                                                            .*%::- .+*.                                                  
                                  +-             :=*%%#+-.  :#%  -=*.            ....                                    
                                  +%+.         -#%%%%%%%%%*:+%+  -%: :=*++++=-:--:-+###*++=:.                            
                                  +-*%:      .#%%@%%%%%%%%%%%%: :*:.=+..                                                 
                                 .+  =%=.   .#%%%%%%%%%%%%%%%#..*--%=.   .::..                                           
                                 +.   :#+.  =%%%%%%%%%%%%%%%%+.*+##: .-+#+=+#%%#+=:.                                     
                                :+##-. .+#: +%%%%%%%%%%%%%%%%##%%+.-*%=.     ..::+%%%###*-.                              
                               .+#*+*#%=..%*+%%%%%%%%%%%%%%%%%@%+*%#.                      :+=:.                         
                             .-**:    .=+%+#%@%%%%%%%%%%%%%%%%%%#=                              .                        
                            =#*:          :+%@@@%%%%%%%%%@@%%%@+.                                                        
                          :*#.       .+@%#%%%%%@%@@@@@@@@%%%%%%:                                                         
                          --      .=#%*:     ..:=+#%@@@@%%%%%%@:                                                         
                        .:.     :#%%+:        :+#%@@#=-..:#%%%%.                                                         
                             .-%%%.      .:#@%@%=.          :: :                                                         
                           :*%%=.    .*%%**-                                                                             
                         .*%%-     .=%%+.                                                                                
                        -%%=.     :#%%.                                                                                  
                       :#%-     .=@%-                                                                                    
                      .*#:     :#@*.                                                                                     
                     .=*.    .+%@-                          ____  _____ _____   ________    ____  ________________  _   __
                    :*.   .=%@*.                          / __ \/ ___//  _/ | / /_  __/   / __ \/ ____/ ____/ __ \/ | / /
                    :*.   .=%@*                          / / / /\__ \ / //  |/ / / /_____/ /_/ / __/ / /   / / / /  |/ / 
                    .=:    =%%=                         / /_/ /___/ // // /|  / / /_____/ _, _/ /___/ /___/ /_/ / /|  /  
                     ..     .*+.                        \____//____/___/_/ |_/ /_/     /_/ |_/_____/\____/\____/_/ |_/   
                             .+-                                                                                                                                                                                                            
                     .        +:                                                                                              
                                +.                                                                                               
                                :.                                                                 
                                  :

     ABOUT:
       Automated OSINT tool for reconnaissance using Google dorking.
       Supports 106 dorks across multiple categories for both domain
       and person-based intelligence gathering.
       And Additional Crawler for a given website.

     TARGET TYPES:
       • DOMAIN MODE: Scan websites, infrastructure, files
       • PERSON MODE: Background checks, social profiles, documents

     QUICK START:
       python osint.py --list              # See all available dorks
       python osint.py -h                  # Show detailed help
       python osint.py -t github.com -d 5  # Run domain dork
       python osint.py -t "John Doe" -d 63 # Run person dork
       python osint.py -t site.com -d 5 --crawl  # With crawler

    LEGAL DISCLAIMER:
       This tool is made just for learning, experimentation, and general OSINT curiosity using publicly available information. 
       It's meant for fun and education only, not for targeting people, invading privacy, or doing anything illegal. 
       Whatever you do with it is your own responsibility, so please use it respectfully and within the law.

    """
    print(Colors.cyan(banner))


def print_all_dorks():
    print("\n" + "=" * 70)
    print(" " * 25 + "AVAILABLE DORKS")
    print("=" * 70)

    domain_dorks = {}
    person_dorks = {}

    for category in DORKS:
        for subcategory in DORKS[category]:
            for num, (name, template, dork_type) in DORKS[category][subcategory].items():
                if dork_type == "domain":
                    if category not in domain_dorks:
                        domain_dorks[category] = {}
                    if subcategory not in domain_dorks[category]:
                        domain_dorks[category][subcategory] = []
                    domain_dorks[category][subcategory].append((num, name, template))
                else:
                    if category not in person_dorks:
                        person_dorks[category] = {}
                    if subcategory not in person_dorks[category]:
                        person_dorks[category][subcategory] = []
                    person_dorks[category][subcategory].append((num, name, template))

    print(Colors.cyan("\nDOMAIN-BASED DORKS (Target: website/company)"))
    print("-" * 70)
    print("Usage: python osint.py -t github.com -d <number>\n")

    for category in sorted(domain_dorks.keys()):
        total = sum(len(domain_dorks[category][sub]) for sub in domain_dorks[category])
        print(Colors.bold(f"\n{category.upper().replace('_', ' ')} ({total} dorks)"))

        for subcategory in sorted(domain_dorks[category].keys()):
            print(f"\n  └─ {subcategory.capitalize()}:")
            for num, name, template in sorted(domain_dorks[category][subcategory]):
                print(f"     {num:3d}: {name}")

    print(Colors.cyan("\n\nPERSON-BASED DORKS (Target: individual's name)"))
    print("-" * 70)
    print('Usage: python osint.py -t "John Doe" -d <number>\n')

    for category in sorted(person_dorks.keys()):
        total = sum(len(person_dorks[category][sub]) for sub in person_dorks[category])
        print(Colors.bold(f"\n{category.upper().replace('_', ' ')} ({total} dorks)"))

        for subcategory in sorted(person_dorks[category].keys()):
            print(f"\n  └─ {subcategory.capitalize()}:")
            for num, name, template in sorted(person_dorks[category][subcategory]):
                print(f"     {num:3d}: {name}")

    print("\n" + "=" * 70)
    print(Colors.yellow("TIP: Use -h for detailed help and more options"))
    print("=" * 70 + "\n")


def find_dork(dork_num):
    for category in DORKS:
        for subcategory in DORKS[category]:
            if dork_num in DORKS[category][subcategory]:
                return DORKS[category][subcategory][dork_num]
    return None


def save_results_json(results, filename, metadata=None):
    try:
        output = {
            'metadata': metadata or {},
            'timestamp': datetime.now().isoformat(),
            'results_count': len(results),
            'results': results
        }

        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(output, f, indent=2, ensure_ascii=False)
        print(Colors.green(f"[+] Results saved to {filename}"))
    except Exception as e:
        print(Colors.red(f"[!] Error saving JSON: {e}"))


def save_results_txt(results, filename, metadata=None):
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(f"OSINT Recon Results\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

            if metadata:
                f.write(f"\nMetadata:\n")
                for key, value in metadata.items():
                    f.write(f"  {key}: {value}\n")

            f.write("=" * 70 + "\n\n")

            for i, item in enumerate(results, 1):
                f.write(f"[{i}] {item['title']}\n")
                f.write(f"URL: {item['link']}\n")
                if 'snippet' in item:
                    f.write(f"Snippet: {item['snippet']}\n")
                f.write("\n" + "-" * 70 + "\n\n")

        print(Colors.green(f"[+] Results saved to {filename}"))
    except Exception as e:
        print(Colors.red(f"[!] Error saving TXT: {e}"))


def validate_domain(domain):
    pattern = r'^[a-zA-Z0-9]([a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(\.[a-zA-Z0-9]([a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$'
    return re.match(pattern, domain) is not None


def main():
    parser = argparse.ArgumentParser(
        description='OSINT Recon - Google Dork Reconnaissance Tool',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python osint.py --list                    # List all dorks
  python osint.py -t github.com -d 5        # Scan domain for ENV files
  python osint.py -t "John Doe" -d 63       # Find LinkedIn profile
  python osint.py -t site.com -d 5 --crawl  # Dork + crawl results
  python osint.py -t site.com -d 5 -p       # Use proxy rotation
  python osint.py -t site.com -d 5 -o results.json  # Save to file
  python osint.py -t site.com -d 5 --depth 2        # Deeper crawling
  python osint.py -t site.com -d 5 --no-robots      # Ignore robots.txt
        """
    )

    parser.add_argument("-t", "--target", help="Target domain or person name")
    parser.add_argument("-d", "--dork", type=int, default=1, help="Dork number (1-106)")
    parser.add_argument("-l", "--list", action="store_true", help="List all available dorks")
    parser.add_argument("--crawl", action="store_true", help="Enable crawler on found URLs")
    parser.add_argument("-p", "--use-proxy", action="store_true", help="Use proxy rotation")
    parser.add_argument("-o", "--output", help="Save results to file (JSON or TXT)")
    parser.add_argument("--depth", type=int, default=1, help="Crawler depth (default: 1)")
    parser.add_argument("--no-robots", action="store_true", help="Ignore robots.txt restrictions")
    parser.add_argument("--max-results", type=int, default=10, help="Maximum results to fetch (default: 10)")

    args = parser.parse_args()

    if len(sys.argv) == 1:
        show_banner()
        sys.exit(0)

    if args.list:
        print_all_dorks()
        sys.exit(0)

    if not args.target:
        print(Colors.red("[!] Error: -t/--target is required when running a dork"))
        print(Colors.yellow("[!] Use --list to see available dorks"))
        print(Colors.yellow("[!] Use -h for help"))
        sys.exit(1)

    dork_info = find_dork(args.dork)

    if dork_info is None:
        print(Colors.red("[!] Invalid Dork number"))
        print(Colors.yellow("[!] Valid Dork numbers are 1-106. Use --list to see all"))
        sys.exit(1)

    name, template, dork_type = dork_info

    if dork_type == "domain":
        if not validate_domain(args.target):
            print(Colors.red("[!] Invalid domain format for domain-based dork"))
            print(Colors.yellow("[!] Domain can only contain: letters, numbers, dots, hyphens"))
            print(Colors.yellow("[!] Example: github.com or api.github.com"))
            print(Colors.yellow(f"[!] Dork #{args.dork} ({name}) requires a domain target"))
            sys.exit(1)

    proxy_manager = None
    if args.use_proxy:
        print(Colors.cyan("\n[*] Initializing proxy system..."))
        proxy_manager = ProxyManager()

        if proxy_manager.fetch_free_proxies():
            proxy_manager.test_all_proxies(max_test=20)

            if proxy_manager.get_working_count() > 0:
                print(Colors.green(f"[+] {proxy_manager.get_working_count()} proxies ready!\n"))
            else:
                print(Colors.yellow("[!] No working proxies found, continuing without them\n"))
                proxy_manager = None
        else:
            print(Colors.yellow("[!] Could not fetch proxies, continuing without them\n"))
            proxy_manager = None

    robot_checker = None
    if args.crawl and not args.no_robots:
        robot_checker = RobotChecker()
        print(Colors.cyan("[*] Robot checker initialized (respecting robots.txt)\n"))

    print(Colors.cyan(f"\n[*] Running: {name}"))
    print(Colors.cyan(f"[*] Type: {'Domain' if dork_type == 'domain' else 'Person'}"))
    print(Colors.cyan(f"[*] Target: {args.target}"))

    query = template.format(target=args.target)
    print(Colors.cyan(f"[*] Search query: {query}"))
    print(Colors.cyan("[*] Searching Google...\n"))

    metadata = {
        'dork_number': args.dork,
        'dork_name': name,
        'dork_type': dork_type,
        'target': args.target,
        'query': query
    }

    url = "https://www.googleapis.com/customsearch/v1"
    params = {
        'key': API_KEY,
        'cx': CX,
        'q': query,
        'num': min(args.max_results, 10)  # Google API max is 10 per request
    }

    try:
        if proxy_manager and proxy_manager.get_working_count() > 0:
            proxy = proxy_manager.get_next_proxy()
            proxies_dict = proxy_manager.get_proxy_dict(proxy)
            print(Colors.yellow(f"[*] Using proxy: {proxy}"))
            response = requests.get(url, params=params, proxies=proxies_dict, timeout=15)
        else:
            response = requests.get(url, params=params, timeout=15)

        response.raise_for_status()
        data = response.json()

        results_list = []

        if 'items' in data:
            print(Colors.green(f"[+] Found {len(data['items'])} results:\n"))

            for i, item in enumerate(data['items'], 1):
                # Print to console
                print(Colors.bold(f"[{i}] {item.get('title', 'No Title')}"))
                print(f"    {item.get('link', 'No Link')}")
                if 'snippet' in item:
                    snippet = item['snippet'][:150]
                    print(Colors.yellow(f"    {snippet}..."))
                print()

                results_list.append(item)

            if args.crawl and results_list:
                print(Colors.cyan("\n[*] Crawler mode enabled!"))
                print(Colors.cyan(f"[*] Crawling {len(results_list)} discovered URLs (depth: {args.depth})...\n"))

                all_crawled = []
                for item in results_list:
                    try:
                        url_to_crawl = item.get('link')
                        if not url_to_crawl:
                            continue

                        print(Colors.cyan(f"[*] Crawling: {url_to_crawl}"))
                        crawled = crawler(
                            url_to_crawl,
                            proxy_manager=proxy_manager,
                            max_depth=args.depth,
                            robot_checker=robot_checker,
                            respect_robots=not args.no_robots
                        )
                        all_crawled.extend(crawled)
                        time.sleep(1)
                    except Exception as e:
                        print(Colors.red(f"[!] Error crawling {item.get('link', 'unknown')}: {e}"))
                        continue

                all_crawled = list(set(all_crawled))

                print(Colors.green(f"\n[+] Crawling complete!"))
                print(Colors.green(f"[+] Original results: {len(results_list)}"))
                print(Colors.green(f"[+] Additional links found: {len(all_crawled)}"))
                print(Colors.green(f"[+] Total URLs discovered: {len(results_list) + len(all_crawled)}\n"))

                if all_crawled:
                    print(Colors.yellow("Sample of discovered URLs:"))
                    for url in all_crawled[:10]:
                        print(Colors.yellow(f"    {url}"))

                    if len(all_crawled) > 10:
                        print(Colors.yellow(f"    ... and {len(all_crawled) - 10} more"))

                metadata['crawled_urls'] = len(all_crawled)

            if args.output:
                if args.output.endswith('.json'):
                    save_results_json(results_list, args.output, metadata)
                else:
                    if not args.output.endswith('.txt'):
                        args.output += '.txt'
                    save_results_txt(results_list, args.output, metadata)
        else:
            print(Colors.yellow("[i] No results found"))

            if 'error' in data:
                error_msg = data['error'].get('message', 'Unknown error')
                print(Colors.red(f"[!] API Error: {error_msg}"))

                if 'quota' in error_msg.lower():
                    print(Colors.yellow("[!] You may have exceeded your daily quota (100 queries/day for free tier)"))
                elif 'invalid' in error_msg.lower():
                    print(Colors.yellow("[!] Check your API key and CX in .env file"))

        print(Colors.cyan("\n[*] Rate limiting: waiting 2 seconds..."))
        time.sleep(2)

        print(Colors.green("\n[+] Scan complete!"))

    except requests.exceptions.Timeout:
        print(Colors.red("[!] Request timeout - the API took too long to respond"))
    except requests.exceptions.HTTPError as e:
        print(Colors.red(f"[!] HTTP Error: {e}"))
        if hasattr(e.response, 'json'):
            try:
                error_data = e.response.json()
                if 'error' in error_data:
                    error_msg = error_data['error'].get('message', 'Unknown error')
                    print(Colors.red(f"[!] API Message: {error_msg}"))

                    if 'quota' in error_msg.lower():
                        print(Colors.yellow("[!] Daily quota exceeded. Free tier allows 100 queries per day."))
                    elif 'invalid' in error_msg.lower() or 'credentials' in error_msg.lower():
                        print(Colors.yellow("[!] Invalid API credentials. Check your .env file."))
            except:
                pass
    except requests.exceptions.RequestException as e:
        print(Colors.red(f"[!] Error making request: {e}"))
    except KeyError as e:
        print(Colors.red(f"[!] Error parsing response: {e}"))
        print(Colors.yellow("[!] Check your API key and CX are correct in .env file"))
    except Exception as e:
        print(Colors.red(f"[!] Unexpected error: {e}"))
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    main()
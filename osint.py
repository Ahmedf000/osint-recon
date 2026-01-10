# WARNING: API keys hardcoded for testing only!
# TO DO/ move .env file before any git commits

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
    banner = """
                                                                                                                                                                                                                                                
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
       And Additional Crawler for A given website.

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
       It’s meant for fun and education only, not for targeting people, invading privacy, or doing anything illegal. 
       Whatever you do with it is your own responsibility, so please use it respectfully and within the law.

    """
    print(Colors.cyan(banner))


def print_all_dorks():
    print("\n" + "=" * 70)
    print(" " * 25 + "AVAILABLE DORKS")
    print("=" * 70)

    # Separate by type
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

    # Print DOMAIN dorks
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

    print(Colors.cyan("\n\n PERSON-BASED DORKS (Target: individual's name)"))
    print("-" * 70)
    print('Usage: python osint.py -t "John Doe" -d <number>\n')

    for category in sorted(person_dorks.keys()):
        total = sum(len(person_dorks[category][sub]) for sub in person_dorks[category])
        print(Colors.bold(f"\n📁 {category.upper().replace('_', ' ')} ({total} dorks)"))

        for subcategory in sorted(person_dorks[category].keys()):
            print(f"\n  └─ {subcategory.capitalize()}:")
            for num, name, template in sorted(person_dorks[category][subcategory]):
                print(f"     {num:3d}: {name}")

    print("\n" + "=" * 70)
    print(Colors.yellow("TIP: Use -h for detailed help and more options"))
    print("=" * 70 + "\n")


def find_dorks(dork_num):

    for category in DORKS:
        for subcategory in DORKS[category]:
            if dork_num in DORKS[category][subcategory]:
                return DORKS[category][subcategory][dork_num]
    return None


def save_results_json(results, filename):
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        print(Colors.green(f"[+] Results saved to {filename}"))
    except Exception as e:
        print(Colors.red(f"[!] Error saving JSON: {e}"))


def save_results_txt(results, filename):
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(f"OSINT Recon Results\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("=" * 70 + "\n\n")

            for item in results:
                f.write(f"Title: {item['title']}\n")
                f.write(f"URL: {item['link']}\n")
                if 'snippet' in item:
                    f.write(f"Snippet: {item['snippet']}\n")
                f.write("\n" + "-" * 70 + "\n\n")

        print(Colors.green(f"[+] Results saved to {filename}"))
    except Exception as e:
        print(Colors.red(f"[!] Error saving TXT: {e}"))


def main():
    parser = argparse.ArgumentParser(
        description='🔍 OSINT Recon - Google Dork Reconnaissance Tool',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python osint.py --list                    # List all dorks
  python osint.py -t github.com -d 5        # Scan domain for ENV files
  python osint.py -t "John Doe" -d 63       # Find LinkedIn profile
  python osint.py -t site.com -d 5 --crawl  # Dork + crawl results
  python osint.py -t site.com -d 5 -p       # Use proxy rotation
  python osint.py -t site.com -d 5 -o results.json  # Save to file
        """
    )

    parser.add_argument("-t", "--target", help="Target domain or person name")
    parser.add_argument("-d", "--dork", type=int, default=1, help="Dork number (1-106)")
    parser.add_argument("-l", "--list", action="store_true", help="List all available dorks")
    parser.add_argument("--crawl", action="store_true", help="Enable crawler on found URLs")
    parser.add_argument("-p", "--use-proxy", action="store_true", help="Use proxy rotation")
    parser.add_argument("-o", "--output", help="Save results to file (JSON or TXT)")
    parser.add_argument("--depth", type=int, default=1, help="Crawler depth (default: 1)")

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

    dork_info = find_dorks(args.dork)

    if dork_info is None:
        print(Colors.red("[!] Invalid Dork number"))
        print(Colors.yellow("[!] Valid Dork numbers are 1-106. Use --list to see all"))
        sys.exit(1)

    name, template, dork_type = dork_info

    if dork_type == "domain":
        if not re.match(r'^[a-zA-Z0-9.-]+$', args.target):
            print(Colors.red("[!] Invalid domain format for domain-based dork"))
            print(Colors.yellow("[!] Domain can only contain: letters, numbers, dots, hyphens"))
            print(Colors.yellow("[!] Example: github.com or api.github.com"))
            print(Colors.yellow(f"[!] Dork #{args.dork} ({name}) requires a domain target"))
            sys.exit(1)
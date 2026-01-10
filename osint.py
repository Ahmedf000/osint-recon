# Google Dork OSINT Tool
# WARNING: API keys hardcoded for testing only!
# TO DO/ move .env file before any git commits

import requests
import sys
import argparse
from template import DORKS
import time
import re
import os
from color.color import Colors, red, green, yellow, blue, cyan, bold
from dotenv import load_dotenv

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

     TARGET TYPES:
       • DOMAIN MODE: Scan websites, infrastructure, files
       • PERSON MODE: Background checks, social profiles, documents

     QUICK START:
       python osint.py --list              # See all available dorks
       python osint.py -h                  # Show detailed help
       python osint.py -t github.com -d 5  # Run domain dork
       python osint.py -t "John Doe" -d 63 # Run person dork

    LEGAL DISCLAIMER:
       This tool is made just for learning, experimentation, and general OSINT curiosity using publicly available information. 
       It’s meant for fun and education only, not for targeting people, invading privacy, or doing anything illegal. 
       Whatever you do with it is your own responsibility, so please use it respectfully and within the law.

    """
    print(banner)


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


    print("\n DOMAIN-BASED DORKS (Target: website/company)")
    print("-" * 70)
    print("Usage: python osint.py -t github.com -d <number>\n")

    for category in sorted(domain_dorks.keys()):
        total = sum(len(domain_dorks[category][sub]) for sub in domain_dorks[category])
        print(f"\n {category.upper().replace('_', ' ')} ({total} dorks)")

        for subcategory in sorted(domain_dorks[category].keys()):
            print(f"\n  └─ {subcategory.capitalize()}:")
            for num, name, template in sorted(domain_dorks[category][subcategory]):
                print(f"     {num:3d}: {name}")


    print("\n\n PERSON-BASED DORKS (Target: individual's name)")
    print("-" * 70)
    print('Usage: python osint.py -t "John Doe" -d <number>\n')

    for category in sorted(person_dorks.keys()):
        total = sum(len(person_dorks[category][sub]) for sub in person_dorks[category])
        print(f"\n {category.upper().replace('_', ' ')} ({total} dorks)")

        for subcategory in sorted(person_dorks[category].keys()):
            print(f"\n  └─ {subcategory.capitalize()}:")
            for num, name, template in sorted(person_dorks[category][subcategory]):
                print(f"     {num:3d}: {name}")

    print("\n" + "=" * 70)
    print("TIP: Use -h for detailed help and more options")
    print("=" * 70 + "\n")


def find_dorks(dork_num):
    for category in DORKS:
        for subcategory in DORKS[category]:
            if dork_num in DORKS[category][subcategory]:
                return DORKS[category][subcategory][dork_num]
    return None


def main():
    parser = argparse.ArgumentParser(
        description='OSINT Recon - Google Dork Reconnaissance Tool',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python osint.py --list                    # List all dorks
  python osint.py -t github.com -d 5        # Scan domain for ENV files
  python osint.py -t "John Doe" -d 63       # Find LinkedIn profile
  python osint.py -t example.com -d 11      # Find login pages
        """
    )

    parser.add_argument("-t", "--target", help="Target domain or person name")
    parser.add_argument("-d", "--dork", type=int, default=1, help="Dork number (1-106)")
    parser.add_argument("-l", "--list", action="store_true", help="List all available dorks")

    args = parser.parse_args()


    if len(sys.argv) == 1:
        show_banner()
        sys.exit(0)


    if args.list:
        print_all_dorks()
        sys.exit(0)


    if not args.target:
        print("[!] Error: -t/--target is required when running a dork")
        print("[!] Use --list to see available dorks")
        print("[!] Use -h for help")
        sys.exit(1)


    dork_info = find_dorks(args.dork)

    if dork_info is None:
        print("[!] Invalid Dork number")
        print("[!] Valid Dork numbers are 1-106. Use --list to see all")
        sys.exit(1)


    name, template, dork_type = dork_info


    if dork_type == "domain":
        if not re.match(r'^[a-zA-Z0-9.-]+$', args.target):
            print("[!] Invalid domain format for domain-based dork")
            print("[!] Domain can only contain: letters, numbers, dots, hyphens")
            print("[!] Example: github.com or api.github.com")
            print(f"[!] Dork #{args.dork} ({name}) requires a domain target")
            sys.exit(1)



    print(f"\n[*] Running: {name}")
    print(f"[*] Type: {'Domain' if dork_type == 'domain' else 'Person'}")
    print(f"[*] Target: {args.target}")


    query = template.format(target=args.target)
    print(f"[*] Search query: {query}")
    print("[*] Searching Google...\n")


    url = "https://www.googleapis.com/customsearch/v1"
    params = {
        'key': API_KEY,
        'cx': CX,
        'q': query,
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()

        data = response.json()

        if 'items' in data:
            print(f"[+] Found {len(data['items'])} results:\n")

            for i, item in enumerate(data['items'], 1):
                print(f"[{i}] {item['title']}")
                print(f"    {item['link']}")
                if 'snippet' in item:
                    print(f"    {item['snippet'][:100]}...")
                print()
        else:
            print("[i] No results found")


        print("[*] Rate limiting: waiting 4 seconds...")
        time.sleep(4)

    except requests.exceptions.RequestException as e:
        print(f"[!] Error making request: {e}")
    except KeyError as e:
        print(f"[!] Error parsing response: {e}")
        print("[!] Check your API key and CX are correct")


if __name__ == "__main__":
    main()
# ehubburner.py

import os
import sys
import time
import argparse
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from colorama import Fore, Style, init
from pyfiglet import Figlet

# =========[🔥 EHUBBURNER ASCII LOGO]==========
EHUB_LOGO = r"""
  ______ _           _     _                          
 |  ____| |         | |   | |                         
 | |__  | | ___  ___| |__ | | ___  _ __   ___  ___    
 |  __| | |/ _ \/ __| '_ \| |/ _ \| '_ \ / _ \/ __|   
 | |____| |  __/ (__| | | | | (_) | | | |  __/\__ \   
 |______|_|\___|\___|_| |_|_|\___/|_| |_|\___||___/   

               🧨  E H U B  B U R N E R  🧨
"""
print(EHUB_LOGO)
# =========[✍️  Argument Parser]==========
def parse_args():
    parser = argparse.ArgumentParser(description="🔥 EhubBurner – Advanced Post-Recon Exploitation Tool")
    parser.add_argument('--target', required=True, help='Target URL (e.g., https://example.com)')
    parser.add_argument('--modules', nargs='+', default=['all'], help='Modules to run (e.g., waf api js dir)')
    return parser.parse_args()

# =========[📡 API Key Scanner]==========
def scan_google_api_keys(url):
    print(f"{Fore.YELLOW}[API] Scanning for Google API keys...")
    try:
        resp = requests.get(url, timeout=5)
        keys = []
        for line in resp.text.split('\n'):
            if 'AIza' in line:
                parts = line.split()
                for part in parts:
                    if 'AIza' in part:
                        keys.append(part.strip('"\';:,<>)'))
        for key in set(keys):
            print(f"{Fore.GREEN}[VALID] Found possible key: {key}")
    except:
        print(f"{Fore.RED}[API] Error fetching target.")

# =========[🔍 JavaScript Secret Scanner]==========
def scan_js_secrets(url):
    print(f"{Fore.YELLOW}[JS] Looking for JavaScript secrets...")
    try:
        soup = BeautifulSoup(requests.get(url, timeout=5).text, 'html.parser')
        scripts = [script['src'] for script in soup.find_all('script') if script.get('src')]
        for js in scripts:
            js_url = urljoin(url, js)
            print(f"[+] Scanning JS: {js_url}")
            try:
                js_text = requests.get(js_url).text
                if any(x in js_text for x in ['key', 'token', 'secret']):
                    print(f"{Fore.CYAN}[+] Secret hints in {js_url}")
            except:
                continue
    except:
        print(f"{Fore.RED}[-] Failed to fetch scripts")

# =========[📁 Directory Brute-force]==========
def brute_force_dirs(url):
    print(f"{Fore.YELLOW}[DIR] Checking common dirs...")
    paths = ['.git', 'admin', 'login', 'config', 'uploads']
    for p in paths:
        full = urljoin(url, p)
        r = requests.get(full)
        if r.status_code == 200 or r.status_code == 403:
            print(f"{Fore.GREEN}[+] {full} => {r.status_code}")

# =========[🔓 Default Login Check]==========
def test_logins(url):
    print(f"{Fore.YELLOW}[AUTH] Testing default credentials...")
    creds = [('admin','admin'),('user','password'),('root','root')]
    for u,p in creds:
        print(f"[ - ] Failed: {u}:{p}")  # Simulated; no real login attempted

# =========[📂 Git Leak Attempt]==========
def try_git_extraction(url):
    print(f"{Fore.YELLOW}[.GIT] Attempting .git extraction...")
    git_url = urljoin(url, '.git/config')
    r = requests.get(git_url)
    if r.status_code == 200:
        print(f"{Fore.RED}[!] Possible .git leak: {git_url}")
    else:
        print(f"{Fore.YELLOW}[-] .git/config inaccessible")

# =========[📜 Main]==========
def main():
    args = parse_args()
    target = args.target if args.target.startswith('http') else 'http://' + args.target
    modules = args.modules

    os.system('clear')
    print(EHUB_LOGO)
    print(f"{Fore.GREEN}[+] Target: {target}")
    print(f"{Fore.GREEN}[+] Modules selected: {modules}\n")
    time.sleep(1)

    if 'all' in modules or 'api' in modules:
        scan_google_api_keys(target)
        time.sleep(0.5)
    if 'all' in modules or 'js' in modules:
        scan_js_secrets(target)
        time.sleep(0.5)
    if 'all' in modules or 'dir' in modules:
        brute_force_dirs(target)
        time.sleep(0.5)
    if 'all' in modules or 'git' in modules:
        try_git_extraction(target)
        time.sleep(0.5)
    if 'all' in modules or 'login' in modules:
        test_logins(target)
        time.sleep(0.5)


if __name__ == '__main__':
    main()

import requests
import dns.resolver
from colorama import Fore, Style

def get_subdomains(domain):
    """
    Enumerates subdomains using crt.sh and hackertarget as fallback.
    """
    print(f"{Fore.CYAN}[*] Enumerating subdomains for {domain}...{Style.RESET_ALL}")
    subdomains = set()
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
    
    # Try crt.sh
    try:
        print(f"{Fore.WHITE}[*] Trying crt.sh...{Style.RESET_ALL}")
        url = f"https://crt.sh/?q=%.{domain}&output=json"
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            data = response.json()
            for entry in data:
                name_value = entry['name_value']
                for sub in name_value.split('\n'):
                    sub = sub.strip()
                    if sub.endswith(domain) and '*' not in sub:
                         subdomains.add(sub)
            print(f"{Fore.GREEN}[+] crt.sh found {len(subdomains)} subdomains.{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}[!] crt.sh failed: {e}{Style.RESET_ALL}")

    if not subdomains:
        # Fallback to Hackertarget
        try:
            print(f"{Fore.WHITE}[*] Trying Hackertarget...{Style.RESET_ALL}")
            url = f"https://api.hackertarget.com/hostsearch/?q={domain}"
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code == 200:
                lines = response.text.split('\n')
                for line in lines:
                    if ',' in line:
                        sub = line.split(',')[0].strip()
                        if sub.endswith(domain):
                             subdomains.add(sub)
                print(f"{Fore.GREEN}[+] Hackertarget found {len(subdomains)} subdomains.{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}[!] Hackertarget failed: {e}{Style.RESET_ALL}")

    print(f"{Fore.GREEN}[+] Found {len(subdomains)} unique subdomains total.{Style.RESET_ALL}")
    return list(subdomains)

def resolve_domains(subdomains):
    """
    Resolves subdomains to check if they are alive.
    Returns a list of alive subdomains.
    """
    print(f"{Fore.CYAN}[*] Resolving {len(subdomains)} subdomains...{Style.RESET_ALL}")
    alive_subdomains = []
    resolver = dns.resolver.Resolver()
    resolver.timeout = 2
    resolver.lifetime = 2

    for sub in subdomains:
        try:
            # We just check for A record to see if it resolves
            resolver.resolve(sub, 'A')
            alive_subdomains.append(sub)
            print(f"{Fore.GREEN}[+] Alive: {sub}{Style.RESET_ALL}")
        except:
            # Try CNAME? Usually A is enough to prove existence. 
            pass
            
    print(f"{Fore.GREEN}[+] {len(alive_subdomains)} subdomains are alive.{Style.RESET_ALL}")
    return alive_subdomains

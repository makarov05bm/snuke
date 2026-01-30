import argparse
import sys
from colorama import init, Fore, Style
from scanner.enum import get_subdomains, resolve_domains
from scanner.crawler import crawl_domain, extract_bucket_urls
from scanner.buckets import check_bucket

# Initialize Colorama
init(autoreset=True)

def banner():
    print(Fore.CYAN + """
   _____             __
  / ___/____  __  __/ /_____
  \__ \/ __ \/ / / / //_/ _ \\
 ___/ / / / / /_/ / ,< /  __/
/____/_/ /_/\__,_/_/|_|\___/
    """ + Style.RESET_ALL)
    print(Fore.WHITE + "    Cloud Storage Bucket Enumerator & Scanner by makarov")
    print(Fore.WHITE + "--------------------------------------------------\n")

def main():
    banner()
    parser = argparse.ArgumentParser(description="Find and scan cloud storage buckets on a target domain.")
    parser.add_argument("domain", help="Target domain (e.g., example.com)")
    args = parser.parse_args()

    target_domain = args.domain

    # 1. Enumeration
    print(f"{Fore.YELLOW}[Phase 1] Enumerating Subdomains for {target_domain}{Style.RESET_ALL}")
    subdomains = get_subdomains(target_domain)
    
    if not subdomains:
        print(f"{Fore.RED}[-] No subdomains found using public sources.{Style.RESET_ALL}")
        # We can still proceed with the main domain itself
        subdomains = [target_domain]
    
    # 2. DNS Resolution
    print(f"\n{Fore.YELLOW}[Phase 2] Verifying Subdomains{Style.RESET_ALL}")
    alive_subdomains = resolve_domains(subdomains)
    
    # Always include the main domain if it resolves
    if target_domain not in alive_subdomains:
         alive_subdomains.append(target_domain)

    if not alive_subdomains:
        print(f"{Fore.RED}[!] No reachable domains found. Exiting.{Style.RESET_ALL}")
        sys.exit(1)

    # 3. Crawling & Bucket Discovery
    print(f"\n{Fore.YELLOW}[Phase 3] Crawling & Hunting for Buckets{Style.RESET_ALL}")
    all_buckets = set()
    
    for sub in alive_subdomains:
        print(f"{Fore.CYAN}[>] Crawling {sub}...{Style.RESET_ALL}")
        content = crawl_domain(sub)
        if content:
            buckets = extract_bucket_urls(content)
            if buckets:
                print(f"{Fore.GREEN}   [+] Found {len(buckets)} potential bucket(s) on {sub}{Style.RESET_ALL}")
                for provider, url in buckets:
                    all_buckets.add((provider, url))
        else:
            print(f"{Fore.RED}   [-] Failed to fetch content from {sub}{Style.RESET_ALL}")

    if not all_buckets:
        print(f"\n{Fore.RED}[-] No bucket URLs found on any subdomain.{Style.RESET_ALL}")
        sys.exit(0)

    # 4. Vulnerability Scanning
    print(f"\n{Fore.YELLOW}[Phase 4] Scanning Discovered Buckets{Style.RESET_ALL}")
    print(f"{Fore.WHITE}[*] Unique buckets found: {len(all_buckets)}{Style.RESET_ALL}\n")
    
    for provider, url in all_buckets:
        check_bucket(provider, url)

    print(f"\n{Fore.CYAN}[*] Scan complete.{Style.RESET_ALL}")

if __name__ == "__main__":
    main()

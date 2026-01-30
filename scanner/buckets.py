import requests
from colorama import Fore, Style
import datetime

POC_FILENAME = "bug_bounty_poc.txt"
POC_CONTENT = f"Bug Bounty POC - Access Check {datetime.datetime.now().isoformat()}"

def check_read_access(bucket_url):
    """
    Checks if a bucket is publicly readable.
    """
    try:
        # Check listing (for S3, listing is often at the root)
        # For Azure/GCP, listing might be different, but a GET on root usually tells us something.
        response = requests.get(bucket_url, timeout=5)
        
        if response.status_code == 200:
            if "ListBucketResult" in response.text or "<Name>" in response.text:
                 return True, "Publicly Listable (Full READ)"
            else:
                 return True, "Publicly Accessible (Maybe just files)"
        elif response.status_code == 403:
            return False, "Access Denied"
        else:
            return False, f"Status: {response.status_code}"
    except Exception as e:
        return False, f"Error: {str(e)}"

def check_write_access(bucket_url):
    """
    Checks if a bucket is writable by attempting to upload a text file.
    """
    target_url = bucket_url.rstrip('/') + "/" + POC_FILENAME
    try:
        # Try PUT
        response = requests.put(target_url, data=POC_CONTENT, timeout=5)
        
        if response.status_code in [200, 201]:
             return True, f"Writable via PUT (Uploaded {POC_FILENAME})"
        else:
             return False, "Not Writable"
    except Exception as e:
        return False, f"Error: {str(e)}"

def check_bucket(provider, bucket_url):
    """
    Orchestrates checks for a single bucket.
    """
    print(f"{Fore.BLUE}[*] Checking {provider} bucket: {bucket_url}{Style.RESET_ALL}")
    
    is_readable, read_msg = check_read_access(bucket_url)
    if is_readable:
        print(f"{Fore.YELLOW}[!] {provider} Bucket READABLE: {bucket_url} ({read_msg}){Style.RESET_ALL}")
    
    is_writable, write_msg = check_write_access(bucket_url)
    if is_writable:
        print(f"{Fore.RED}[!!!] {provider} Bucket WRITABLE: {bucket_url} ({write_msg}){Style.RESET_ALL}")
        
    if not is_readable and not is_writable:
        print(f"{Fore.WHITE}[-] {bucket_url} is secure or not accessible.{Style.RESET_ALL}")

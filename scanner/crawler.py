import requests
import re
from colorama import Fore, Style
from urllib.parse import urljoin

# Regex patterns for common storage buckets
BUCKET_PATTERNS = {
    'AWS': r'(?:https?://)?(?:s3(?:[.-][a-z0-9-]+)?\.amazonaws\.com/[a-z0-9._-]+|[a-z0-9._-]+\.s3(?:[.-][a-z0-9-]+)?\.amazonaws\.com|[a-z0-9._-]+\.s3-website(?:[.-][a-z0-9-]+)?\.amazonaws\.com)',
    'Azure': r'(?:https?://)?(?:[a-z0-9]+\.blob\.core\.windows\.net|[a-z0-9]+\.dfs\.core\.windows\.net|[a-z0-9]+\.file\.core\.windows\.net|[a-z0-9]+\.queue\.core\.windows\.net|[a-z0-9]+\.table\.core\.windows\.net)',
    'GCP': r'(?:https?://)?(?:storage\.googleapis\.com/[a-z0-9._-]+|[a-z0-9._-]+\.storage\.googleapis\.com|storage\.cloud\.google\.com/[a-z0-9._-]+)'
}

def crawl_domain(subdomain):
    """
    Fetches the content of the subdomain and searches for bucket URLs.
    Tries both http and https.
    """
    protocols = ['https', 'http']
    content = ""
    
    for proto in protocols:
        url = f"{proto}://{subdomain}"
        try:
            response = requests.get(url, timeout=5)
            content += response.text
            # If we successfully got content, we can probably stop, but traversing both might be better if they serve different things?
            # Usually https is preferred. If https works, we might just stick with it.
            if response.status_code == 200:
                break 
        except:
            continue
            
    return content

def extract_bucket_urls(content):
    """
    Scans the HTML/JS content for cloud storage bucket URLs.
    """
    found_buckets = set()
    
    for provider, pattern in BUCKET_PATTERNS.items():
        matches = re.findall(pattern, content)
        for match in matches:
            # Cleanup and normalization could happen here
            # For now we assume the regex captures the host or host/path
            
            # Construct a full URL if it's just a domain
            if match.startswith('http'):
                found_buckets.add((provider, match))
            else:
                # Default to https
                found_buckets.add((provider, f"https://{match}"))
                
    return list(found_buckets)

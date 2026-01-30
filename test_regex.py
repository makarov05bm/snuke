import re
from scanner.crawler import BUCKET_PATTERNS, extract_bucket_urls

test_cases = {
    'AWS': [
        "https://mybucket.s3.amazonaws.com",
        "http://s3.amazonaws.com/mybucket",
        "s3-us-west-1.amazonaws.com/mybucket",
        "mybucket.s3-website-us-east-1.amazonaws.com",
        "mybucket.s3.eu-central-1.amazonaws.com"
    ],
    'Azure': [
        "myaccount.blob.core.windows.net",
        "https://myaccount.dfs.core.windows.net",
        "http://myaccount.file.core.windows.net",
        "myaccount.queue.core.windows.net",
        "myaccount.table.core.windows.net"
    ],
    'GCP': [
        "storage.googleapis.com/mybucket",
        "mybucket.storage.googleapis.com",
        "https://storage.cloud.google.com/mybucket"
    ]
}

def test_patterns():
    print("Testing Bucket Regex Patterns...")
    failures = 0
    
    for provider, urls in test_cases.items():
        print(f"\n--- Testing {provider} ---")
        pattern = BUCKET_PATTERNS[provider]
        for url in urls:
            # Simulate finding it in some text
            fake_html = f"Here is a link to {url} inside a page."
            found = extract_bucket_urls(fake_html)
            
            # extract_bucket_urls finds ALL providers, so we just check if our expected URL is in there
            # extract_bucket_urls returns tuples of (provider, url)
            
            match_found = False
            for p, u in found:
                if p == provider and (url in u or u in url): # Simple containment check as logic adds https://
                    match_found = True
                    print(f"[PASS] Matched {url} -> {u}")
                    break
            
            if not match_found:
                print(f"[FAIL] Did not match {url}")
                failures += 1
                
    if failures == 0:
        print("\nAll tests passed!")
    else:
        print(f"\n{failures} tests failed.")

if __name__ == "__main__":
    test_patterns()

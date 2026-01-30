import requests

def debug_crt(domain):
    url = f"https://crt.sh/?q=%.{domain}&output=json"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
    print(f"Querying crt.sh: {url}")
    try:
        response = requests.get(url, headers=headers, timeout=20)
        print(f"crt.sh Status Code: {response.status_code}")
        if response.status_code == 200:
             print("crt.sh Success")
             return
    except Exception as e:
        print(f"crt.sh Error: {e}")

    print("Trying Hackertarget fallback...")
    ht_url = f"https://api.hackertarget.com/hostsearch/?q={domain}"
    try:
        response = requests.get(ht_url, headers=headers, timeout=20)
        print(f"Hackertarget Status Code: {response.status_code}")
        print("Response preview:")
        print(response.text[:200])
    except Exception as e:
        print(f"Hackertarget Error: {e}")

if __name__ == "__main__":
    debug_crt("louisvuitton.com")

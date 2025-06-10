import requests
import random
from concurrent.futures import ThreadPoolExecutor
import time

REQUIRED_PROXIES = 500
PROXIES_PER_SOURCE = 150

# مصادر بروكسيات أوروبية فقط
PROXY_SOURCES = [
    "https://raw.githubusercontent.com/mmpx12/proxy-list/master/http.txt",
    "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt",
    "https://raw.githubusercontent.com/roosterkid/openproxylist/main/HTTPS_RAW.txt",
]

def fetch_proxies_from_source(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        proxies = list(set(response.text.strip().splitlines()))
        return proxies[:PROXIES_PER_SOURCE]
    except Exception as e:
        print(f"[!] Failed to fetch from {url}: {e}")
        return []

def test_proxy(proxy):
    try:
        response = requests.get(
            "https://ipinfo.io/json",
            proxies={"http": f"http://{proxy}", "https": f"http://{proxy}"},
            timeout=5,
        )
        data = response.json()
        country = data.get("country", "")
        if country in ["DE", "FR", "NL", "SE", "NO", "FI", "IT", "ES", "BE", "CH", "AT", "DK", "IE", "GB", "PL"]:
            return proxy
    except:
        pass
    return None

def get_working_proxies(required=REQUIRED_PROXIES):
    final_proxies = set()
    tried_sources = set()

    while len(final_proxies) < required:
        print(f"\n[*] Looking for proxies... {len(final_proxies)}/{required}")

        all_candidates = set()
        for source in PROXY_SOURCES:
            if source in tried_sources:
                continue
            candidates = fetch_proxies_from_source(source)
            all_candidates.update(candidates)
            tried_sources.add(source)

        if not all_candidates:
            print("[!] No new proxies fetched. Retrying in 10 seconds...")
            time.sleep(10)
            tried_sources.clear()
            continue

        print(f"[+] Testing {len(all_candidates)} proxies...")
        with ThreadPoolExecutor(max_workers=100) as executor:
            results = list(executor.map(test_proxy, all_candidates))

        valid = set(filter(None, results))
        final_proxies.update(valid)

        if len(final_proxies) >= required:
            print(f"[✓] Found {len(final_proxies)} valid proxies.")
            break
        else:
            print(f"[-] Only {len(final_proxies)} valid so far. Retrying...")

        time.sleep(5)
        tried_sources.clear()

    return list(final_proxies)[:required]

if __name__ == "__main__":
    proxies = get_working_proxies()
    for proxy in proxies:
        print(proxy)

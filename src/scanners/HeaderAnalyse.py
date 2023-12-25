import requests
from colorama import Fore, Style
from tqdm import tqdm

def scan_headers(target_domain):
    try:
        url = f"https://{target_domain}"

        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.79 Safari/537.36",
        }

        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            print(f"Scanning {url}")
            required_headers = {"strict-transport-security", "content-security-policy", "x-frame-options", "x-content-type-options", "referrer-policy", "X-XSS-Protection", "Public-Key-Pins", "Expect-CT"}
            actual_headers = set(header.lower() for header in response.headers.keys())
            missing_headers = required_headers - actual_headers

            if missing_headers:
                print(Fore.RED + f"Missing security headers on {url}: {', '.join(missing_headers)}")
                print(Style.RESET_ALL)
            else:
                print(Fore.RED + f"All required security headers present on {url}")
                print(Style.RESET_ALL)

            with tqdm(total=len(required_headers), desc="Scanning headers") as pbar:
                for vuln in required_headers:
                    pbar.update(1)

    except requests.exceptions.RequestException as e:
        print(f"Error scanning {target_domain}: {e}")


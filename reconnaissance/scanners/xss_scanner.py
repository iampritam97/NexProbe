import requests
import re
import yaml
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor

def get_urls(domain):
    # Get all the URLs from archive.org.
    response = requests.get(
        f"https://web.archive.org/cdx/search/cdx?url={domain}/*&output=json&fl=original&collapse=urlkey")
    data = response.json()
    urls = [entry[0] if entry[0].startswith('http') else 'https://' + entry[0] for entry in
            data]  # Add 'https://' if no scheme
    return urls

def scan_url(url, vulnerabilities):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            for vuln in vulnerabilities:
                name = vuln["name"]
                pattern = vuln["pattern"]
                matcher = vuln["matcher"]
                payload = vuln.get("payload", "")  # Get the payload field or an empty string if not provided
                # payload_matcher = vuln.get("payload_matcher", None)
                #
                # if payload_matcher and re.search(payload_matcher, response.text, re.IGNORECASE):
                #    print(f"Skipping URL {url} as it matches a payload_matcher")
                #    continue

                new_url = url.replace('=', '=' + payload)
                # print(new_url)
                response2 = requests.get(new_url + pattern)
                if re.search(matcher, response2.text, re.IGNORECASE):
                    # if re.search(payload, response2.text, re.IGNORECASE):
                    print(f"Potential XSS detected on {url}: {name}")
    except requests.exceptions.RequestException as e:
        print(f"Error scanning {url}: {e}")

def scan_for_xss(urls, vulnerabilities):
    with tqdm(total=len(urls), unit="URLs", desc="Scanning URLs") as pbar, ThreadPoolExecutor() as executor:
        futures = [executor.submit(scan_url, url, vulnerabilities) for url in urls]
        for future in futures:
            future.result()  # Wait for each task to complete
            pbar.update(1)


def main():
    target_domain = input("Enter the target domain (e.g., example.com): ")
    domain_urls = get_urls(target_domain)

    # Load the vulnerability patterns from the configuration file
    with open("configs/xss_config.yaml", "r") as config_file:
        vulnerabilities = yaml.safe_load(config_file)

    scan_for_xss(domain_urls, vulnerabilities)


if __name__ == "__main__":
    main()

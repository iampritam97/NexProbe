import os
import requests
import re
import yaml
from colorama import Fore, Back, Style
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor

def xss(target_domain):
    def get_urls(domain):
        response = requests.get(
            f"https://web.archive.org/cdx/search/cdx?url={domain}/*&output=json&fl=original&collapse=urlkey")
        data = response.json()
        urls = [entry[0] if entry[0].startswith('http') else 'https://' + entry[0] for entry in
                data]
        return urls

    def scan_url(url, vulnerabilities, results):
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
                        results.append(url)
                        print(Fore.RED + f"Potential XSS detected on {url}: {name}")
                        print(Style.RESET_ALL)
        except requests.exceptions.RequestException as e:
            print(f"Error scanning {url}: {e}")

    def scan_for_xss(urls, vulnerabilities):
        vulnerable_urls = []
        with tqdm(total=len(urls), unit="URLs", desc="Scanning URLs") as pbar, ThreadPoolExecutor() as executor:
            futures = [executor.submit(scan_url, url, vulnerabilities, vulnerable_urls) for url in urls]
            for future in futures:
                future.result()
                pbar.update(1)

        return vulnerable_urls
    domain_urls = get_urls(target_domain)

    script_directory = os.path.dirname(os.path.realpath(__file__))
    config_file_path = os.path.join(script_directory, "configs", "xss_config.yaml")
    with open(config_file_path, "r") as config_file:
        vulnerabilities = yaml.safe_load(config_file)

    vulnerable_urls = scan_for_xss(domain_urls, vulnerabilities)
    with open("vulnerable_xss_urls.txt", "w") as output_file:
        for url in vulnerable_urls:
            output_file.write(url + '\n')

    print(Fore.RED + f"{len(vulnerable_urls)} vulnerable URLs have been saved to vulnerable_xss_urls.txt")
    print(Style.RESET_ALL)



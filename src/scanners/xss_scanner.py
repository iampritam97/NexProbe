import os
import requests
import re
import yaml
from colorama import Fore, Style
from concurrent.futures import ThreadPoolExecutor
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet


def xss(target_domain):
    def get_urls(domain):
        response = requests.get(
            f"https://web.archive.org/cdx/search/cdx?url={domain}/*&output=json&fl=original&collapse=urlkey", timeout=10)
        data = response.json()
        urls = [entry[0] if entry[0].startswith('http') else 'https://' + entry[0] for entry in
                data]
        return urls

    def scan_url(url, vulnerabilities, results):
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                for vuln in vulnerabilities:
                    name = vuln["name"]
                    pattern = vuln["pattern"]
                    matcher = vuln["matcher"]
                    payload = vuln.get("payload", "")
                    # payload_matcher = vuln.get("payload_matcher", None)
                    #
                    # if payload_matcher and re.search(payload_matcher, response.text, re.IGNORECASE):
                    #    print(f"Skipping URL {url} as it matches a payload_matcher")
                    #    continue

                    new_url = url.replace('=', '=' + payload)
                    # print(new_url)
                    response2 = requests.get(new_url + pattern, timeout=10)
                    if re.search(matcher, response2.text, re.IGNORECASE):
                        # if re.search(payload, response2.text, re.IGNORECASE):
                        results.append(url)
                        print(Fore.GREEN + f"Potential XSS detected on {url}: {name}")
                        print(Style.RESET_ALL)
        except requests.exceptions.RequestException as e:
            print(f"Error scanning {url}")

    def scan_for_xss(urls, vulnerabilities):
        vulnerable_urls = []
        with ThreadPoolExecutor() as executor:
            futures = [executor.submit(scan_url, url, vulnerabilities, vulnerable_urls) for url in urls]
            for future in futures:
                future.result()

        return vulnerable_urls

    def create_pdf(vulnerable_urls, domain):
        output_directory = 'output'
        output_pdf_file = os.path.join(output_directory, 'XSS_Scan_Report.pdf')

        output_dir = os.path.dirname(output_pdf_file)
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        doc = SimpleDocTemplate(output_pdf_file, pagesize=letter)
        styles = getSampleStyleSheet()

        story = []
        title = Paragraph(f"<b>XSS Scan for {domain}</b>", styles['Title'])
        story.append(title)
        story.append(Paragraph("<b>Vulnerable URLs:</b>", styles['Normal']))
        for url in vulnerable_urls:
            story.append(Paragraph(url, styles['Normal']))

        doc.build(story)

        print(Fore.RED + f"PDF report with vulnerable URLs saved to: {output_pdf_file}" + Style.RESET_ALL)

    domain_urls = get_urls(target_domain)

    script_directory = os.path.dirname(os.path.realpath(__file__))
    config_file_path = os.path.join(script_directory, "configs", "xss_config.yaml")
    with open(config_file_path, "r") as config_file:
        vulnerabilities = yaml.safe_load(config_file)

    vulnerable_urls = scan_for_xss(domain_urls, vulnerabilities)
    create_pdf(vulnerable_urls, target_domain)

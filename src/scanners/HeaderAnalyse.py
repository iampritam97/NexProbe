import os

import requests
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from colorama import Fore, Style


def scan_headers(target_domain):
    try:
        url = f"https://{target_domain}"

        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.79 Safari/537.36",
        }

        response = requests.get(url, headers=headers, timeout=10)

        if response.status_code == 200:
            print(Fore.GREEN + f"Scanning {url}")
            required_headers = {"strict-transport-security", "content-security-policy", "x-frame-options",
                                "x-content-type-options", "referrer-policy", "X-XSS-Protection", "Public-Key-Pins",
                                "Expect-CT"}
            actual_headers = set(header.lower() for header in response.headers.keys())
            missing_headers = required_headers - actual_headers

            if missing_headers:
                print(f"Missing security headers on {url}: {', '.join(missing_headers)}")
                Style.RESET_ALL
            else:
                print(Fore.GREEN + f"All required security headers present on {url}")
                print(Style.RESET_ALL)

            create_pdf(missing_headers, target_domain)

    except requests.exceptions.RequestException as e:
        print(f"Error scanning {target_domain}: {e}")


def create_pdf(missing_headers, target_domain):
    output_directory = 'output'
    output_pdf_file = os.path.join(output_directory, 'Header_Scan_Report.pdf')

    output_dir = os.path.dirname(output_pdf_file)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    doc = SimpleDocTemplate(output_pdf_file, pagesize=letter)
    styles = getSampleStyleSheet()

    story = []
    title = Paragraph(f"<b>Header Analysis for {target_domain}</b>", styles['Title'])
    story.append(title)

    for header in missing_headers:
        story.append(Paragraph(f"<b>Missing Header:</b> {header}", styles['Normal']))

    doc.build(story)

    print(Fore.RED + f"Report for header analysis saved to: {output_pdf_file}" + Style.RESET_ALL)

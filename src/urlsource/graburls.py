import os
import requests
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from colorama import Fore, Style

def get_urls(domain):
    response = requests.get(
        f"https://web.archive.org/cdx/search/cdx?url={domain}/*&output=json&fl=original&collapse=urlkey", timeout=10)
    data = response.json()

    urls = [entry[0] for entry in data]

    return urls


def fetch_urls(domain):
    urls = get_urls(domain)
    print(Fore.GREEN + f"URLs for {domain}")
    for i in urls:
        print(i)
    Style.RESET_ALL
    create_pdf(urls, "URLs_Report.pdf", domain)

    print(Fore.RED + f"URLs report have been saved to output folder.")
    Style.RESET_ALL


def create_pdf(urls, output_file, domain):
    output_directory = 'output'
    output_pdf_file = os.path.join(output_directory, output_file)

    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    pdf = SimpleDocTemplate(output_pdf_file, pagesize=letter)
    story = []

    styles = getSampleStyleSheet()
    story.append(Paragraph("Web Archive URLs Report", styles['Title']))
    story.append(Paragraph(f"Domain: {domain}", styles['Normal']))
    story.append(Spacer(1, 12))

    for url in urls:
        story.append(Paragraph(f"URL: {url}", styles['Normal']))

    pdf.build(story)

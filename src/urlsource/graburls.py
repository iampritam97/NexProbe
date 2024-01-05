import os
import requests
from colorama import Style
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet


def get_urls(domain):
    response = requests.get(
        f"https://web.archive.org/cdx/search/cdx?url={domain}/*&output=json&fl=original&collapse=urlkey")
    data = response.json()

    urls = [entry[0] for entry in data]

    return urls


def fetch_urls(domain):
    urls = get_urls(domain)

    create_pdf(urls, "URLs_Report.pdf", domain)

    print(f"URLs and PDF report have been generated.")
    print(Style.RESET_ALL)


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

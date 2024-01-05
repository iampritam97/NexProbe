import os

import requests
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from colorama import Fore

def hunter_fetch_emails(domain):
    api_key = "61150cc37813ef999eba7556f301b88e98b12061"
    url = f"https://api.hunter.io/v2/domain-search?domain={domain}&api_key={api_key}"

    response = requests.get(url)
    data = response.json() if response.status_code == 200 else {}

    emails = [email.get("value") for email in data.get("data", {}).get("emails", [])]

    for email in emails:
        print(Fore.RED + email)

    create_pdf(emails)
def create_pdf(emails):
    output_directory = 'output'
    output_pdf_file = os.path.join(output_directory, 'Email_Report_Hunter.pdf')

    output_dir = os.path.dirname(output_pdf_file)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    doc = SimpleDocTemplate(output_pdf_file, pagesize=letter)
    styles = getSampleStyleSheet()

    story = []
    title = Paragraph(f"<b>Fetched Emails - Hunter.io</b>", styles['Title'])
    story.append(title)
    for email in emails:
        story.append(Paragraph(f"<b>Email:</b> {email}", styles['Normal']))

    doc.build(story)

    print(f"PDF report with emails saved to: {output_pdf_file}")

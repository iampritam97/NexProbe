import os

import requests
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from colorama import Fore, Style


def detect_techstack(domain):
    api_key = 'wllsc86oe0gsvl2t3mshsrxq2k7ne9i6821spgc7acb8f9lyilv4nlbes2k8uioi4brz2m'
    base_url = f"https://whatcms.org/API/Tech?key={api_key}&url={domain}"

    params = {
        "url": domain,
    }

    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()

        data = response.json()

    except requests.exceptions.RequestException as e:
        print(f"Error detecting technology stack for {domain}: {e}")
        return None

    if data and "results" in data:
        results = data["results"]
        print(Fore.RED + f"Technology used for {domain}:")
        for result in results:
            name = result.get("name")
            if name:
                print(Fore.RED + f" - {name}")

        create_pdf(results, domain)

    else:
        print(Fore.RED + "No technology information available.")
        print(Style.RESET_ALL)


def create_pdf(results, domain):
    output_directory = 'output'
    output_pdf_file = os.path.join(output_directory, 'TechStack_Report.pdf')

    output_dir = os.path.dirname(output_pdf_file)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    doc = SimpleDocTemplate(output_pdf_file, pagesize=letter)
    styles = getSampleStyleSheet()

    story = []
    title = Paragraph(f"<b>TechStack Report for {domain}</b>", styles['Title'])
    story.append(title)
    for result in results:
        name = result.get("name")
        if name:
            story.append(Paragraph(f"<b>Technology Used:</b> {name}", styles['Normal']))

    doc.build(story)

    print(f"PDF report with technology stack saved to: {output_pdf_file}")

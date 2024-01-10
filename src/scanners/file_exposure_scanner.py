import os
import requests
import re
import yaml
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from colorama import Fore, Style

script_directory = os.path.dirname(os.path.realpath(__file__))
config_file_path = os.path.join(script_directory, "configs", "file_exposure_config.yaml")
with open(config_file_path, "r") as config_file:
    vulnerabilities = yaml.safe_load(config_file)


def file_exposure(target_domain):
    exposed_files = []

    try:
        response = requests.get(f"https://{target_domain}")
        if response.status_code == 200:
            for vuln in vulnerabilities:
                name = vuln["name"]
                pattern = vuln["pattern"]
                matcher = vuln["matcher"]
                response2 = requests.get(f"https://{target_domain}{pattern}")
                if re.search(matcher, response2.text, re.IGNORECASE):
                    exposed_files.append(f"{target_domain}{pattern}: {name}")
                    print(Fore.GREEN + f"File exposure detected on {target_domain}{pattern}: {name}")
                    print(Style.RESET_ALL)

            create_pdf(exposed_files, target_domain)
    except requests.exceptions.RequestException as e:
        print(f"Error scanning {target_domain}: {e}")


def create_pdf(exposed_files, target_domain):
    output_directory = 'output'
    output_pdf_file = os.path.join(output_directory, 'File_Exposure_Report.pdf')

    output_dir = os.path.dirname(output_pdf_file)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    doc = SimpleDocTemplate(output_pdf_file, pagesize=letter)
    styles = getSampleStyleSheet()

    story = []
    title = Paragraph(f"<b>File Exposures for {target_domain}</b>", styles['Title'])
    story.append(title)
    for exposed_file in exposed_files:
        story.append(Paragraph(f"<b>Exposed File:</b> {exposed_file}", styles['Normal']))

    doc.build(story)

    print(Fore.RED + f"Report with exposed files saved to: {output_pdf_file}" + Style.RESET_ALL)

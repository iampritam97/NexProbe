import os
import requests
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from colorama import Fore, Style

script_directory = os.path.dirname(os.path.realpath(__file__))
wordlist_file_path = os.path.join(script_directory, "configs", "wordlist.txt")

def load_wordlist(file_path):
    with open(file_path, "r") as wordlist_file:
        return [line.strip() for line in wordlist_file]


def dir_exposure(target_domain):
    exposed_dir = []

    try:
        response = requests.get(f"https://{target_domain}", timeout=10)
        if response.status_code == 200:
            wordlist = load_wordlist(wordlist_file_path)
            for directory in wordlist:
                response2 = requests.get(f"https://{target_domain}/{directory}", timeout=10)
                if response2.status_code == 200:
                    exposed_dir.append(f"{target_domain}/{directory}")
                    print(Fore.GREEN + f"Directory exposure detected on {target_domain}/{directory}")
                    print(Style.RESET_ALL)

            create_pdf(exposed_dir, target_domain)
    except requests.exceptions.RequestException as e:
        print(f"Error scanning {target_domain}: {e}")


def create_pdf(exposed_dir, target_domain):
    output_directory = 'output'
    output_pdf_file = os.path.join(output_directory, 'Dir_Exposure_Report.pdf')

    output_dir = os.path.dirname(output_pdf_file)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    doc = SimpleDocTemplate(output_pdf_file, pagesize=letter)
    styles = getSampleStyleSheet()

    story = []
    title = Paragraph(f"<b>Exposed directories for {target_domain}</b>", styles['Title'])
    story.append(title)
    for exposed_dirs in exposed_dir:
        story.append(Paragraph(f"<b>Exposed directories:</b> {exposed_dir}", styles['Normal']))

    doc.build(story)

    print(Fore.RED + f"Report with exposed directories saved to: {output_pdf_file}" + Style.RESET_ALL)
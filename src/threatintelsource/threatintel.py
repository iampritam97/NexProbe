import os
import requests
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from colorama import Fore, Style

OTX_API_KEY = "81332555b6860a7b0ef047757fa704037517158e7dedca1494a676866f0d1cfd"

OTX_API_URL = "https://otx.alienvault.com/api/v1/indicators/domain/{indicator}/{section}"


def print_and_save_to_pdf(output_text, output_pdf_file):
    print(Fore.GREEN + output_text + Style.RESET_ALL)

    doc = SimpleDocTemplate(output_pdf_file, pagesize=letter)
    styles = getSampleStyleSheet()

    story = []

    title = Paragraph("<b>AlienVault URL Threat Intelligence</b>", styles['Title'])
    story.append(title)

    story.append(Paragraph(output_text, styles['Normal']))

    doc.build(story)

    print(Fore.RED + f"AlienVault OTX Threat intelligence report saved to: {output_pdf_file}" + Style.RESET_ALL)


def query_alienvault_otx(indicator, section="url_list"):
    try:
        headers = {"OTX_API_KEY": OTX_API_KEY}
        url = OTX_API_URL.format(indicator=indicator, section=section)

        response = requests.get(url, headers=headers, timeout=10)

        if response.status_code == 200:
            data = response.json()
            output_text = ""

            if data.get('size', 0) == 0 and data.get('count', 0) == 0:
                output_text = "No threat vector found."
            else:
                output_text = "Threat Intelligence Data:\n"
                for entry in data.get("data", []):
                    output_text += f"Datetime Int: {entry.get('datetime_int', 'N/A')}\n"
                    output_text += f"Hash: {entry.get('hash', 'N/A')}\n"
                    detections = entry.get('detections', {})
                    output_text += "Detections:\n"
                    output_text += f"  Avast: {detections.get('avast', 'N/A')}\n"
                    output_text += f"  AVG: {detections.get('avg', 'N/A')}\n"
                    output_text += f"  ClamAV: {detections.get('clamav', 'N/A')}\n"
                    output_text += f"  MS Defender: {detections.get('msdefender', 'N/A')}\n"
                    output_text += f"Date: {entry.get('date', 'N/A')}\n\n"

            output_directory = 'output'
            output_pdf_file = os.path.join(output_directory, 'AlienVault_URLsThreatIntel_Report_.pdf')

            output_dir = os.path.dirname(output_pdf_file)
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)

            print_and_save_to_pdf(output_text, output_pdf_file)

        else:
            print(f"Failed to retrieve threat intelligence for {indicator}. Status Code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")

import os
import requests
import time
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from colorama import Fore, Style


def pulsedive_domain_info(api_key, pretty, probe, domain):
    base_url = "https://pulsedive.com/api/analyze.php"
    endpoint = f"value={domain}"

    params = {
        "probe": probe,
        "pretty": pretty,
        "key": api_key,
    }

    try:
        response = requests.get(f"{base_url}?{endpoint}", params=params)
        response.raise_for_status()

        data = response.json()
        qid = data.get('qid')

        if qid:
            print(Fore.GREEN + f"Added request to queue. QID: {qid}" + Style.RESET_ALL)
            return qid
        else:
            print("Failed to retrieve QID.")
            return None

    except requests.exceptions.RequestException as e:
        print(f"Error fetching information for {domain}: {e}")
        return None


def get_info_by_qid(api_key, pretty, qid):
    base_url = "https://pulsedive.com/api/analyze.php"
    params = {
        "qid": qid,
        "pretty": pretty,
        "key": api_key,
    }

    try:
        time.sleep(60)
        response = requests.get(base_url, params=params)
        response.raise_for_status()

        data = response.json()
        return data

    except requests.exceptions.RequestException as e:
        print(f"Error fetching information for QID {qid}: {e}")
        return None


def create_pdf(domain, info_by_qid, output_file, api_key, qid):
    output_directory = 'output'
    output_pdf_file = os.path.join(output_directory, output_file)

    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    pdf = SimpleDocTemplate(output_pdf_file, pagesize=letter)
    story = []

    styles = getSampleStyleSheet()
    story.append(Paragraph("Pulsedive Domain Information Report", styles['Title']))
    story.append(Paragraph(f"Domain: {domain}", styles['Normal']))
    story.append(Spacer(1, 12))

    if info_by_qid:
        if 'data' in info_by_qid:
            info = info_by_qid['data']
            risk = info.get('risk')
            indicator = info.get('indicator')
            indicator_type = info.get('type')
            stamp_probed = info.get('stamp_probed')
            if risk and indicator and indicator_type and stamp_probed:
                story.append(Paragraph(f"Risk: {risk}", styles['Normal']))
                story.append(Paragraph(f"Indicator: {indicator}", styles['Normal']))
                story.append(Paragraph(f"Type: {indicator_type}", styles['Normal']))
                story.append(Paragraph(f"Stamp Probed: {stamp_probed}", styles['Normal']))
                print(Fore.GREEN + "Pulsedive Information:")
                print(f"Risk: {risk}")
                print(f"Indicator: {indicator}")
                print(f"Type: {indicator_type}")
                print(f"Stamp Probed: {stamp_probed}" + Style.RESET_ALL)
            else:
                print(Fore.GREEN + "Risk or Indicator not found in the response." + Style.RESET_ALL)
                story.append(Paragraph("Risk or Indicator not found in the response.", styles['Normal']))
    else:
        story.append(Paragraph("Failed to retrieve information.", styles['Normal']))
    story.append(Paragraph(f"More Info: https://pulsedive.com/api/analyze.php?qid={qid}&pretty=1&key={api_key}"))

    pdf.build(story)


def pulsedive_main(domain):
    api_key = '1556048602b2c4dfa51c1913685655a8715d21dbd8a5703d3852aacfc4ba16e5'
    pretty = '1'
    probe = '1'
    qid = pulsedive_domain_info(api_key, pretty, probe, domain)

    if qid:
        print(Fore.GREEN + f"Waiting for 1 minute..." + Style.RESET_ALL)
        time.sleep(60)

        info_by_qid = get_info_by_qid(api_key, pretty, qid)

        create_pdf(domain, info_by_qid, "Pulsedive_Report.pdf", api_key, qid)

        print(Fore.RED + f"Pulsedive information and PDF report have been saved to output folder." + Style.RESET_ALL)
    else:
        print("Failed to retrieve QID. Exiting.")

import os

import requests
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from colorama import Fore,Style

def create_pdf(domain_report, output_file):
    output_dir = os.path.dirname(output_file)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    doc = SimpleDocTemplate(output_file, pagesize=letter)
    styles = getSampleStyleSheet()
    centered_title_style = ParagraphStyle(
        'CenteredTitle',
        parent=styles['Title'],
        alignment=TA_CENTER,
    )

    story = []

    title = Paragraph(f"<b>VirusTotal Domain Report - {domain_report['data']['id']}</b>", centered_title_style)
    story.append(title)
    story.append(Paragraph(f"<b>Domain:</b> {domain_report['data']['id']}", styles['Normal']))
    story.append(Paragraph(f"<b>Last Analysis Date:</b> {domain_report['data']['attributes']['last_analysis_date']}",
                           styles['Normal']))
    story.append(Paragraph("<b>Analysis Status:</b>", styles['Heading2']))
    story.append(Paragraph(f"<b>Harmless:</b> {domain_report['data']['attributes']['last_analysis_stats']['harmless']}",
                           styles['Normal']))
    story.append(
        Paragraph(f"<b>Malicious:</b> {domain_report['data']['attributes']['last_analysis_stats']['malicious']}",
                  styles['Normal']))
    story.append(
        Paragraph(f"<b>Suspicious:</b> {domain_report['data']['attributes']['last_analysis_stats']['suspicious']}",
                  styles['Normal']))
    story.append(
        Paragraph(f"<b>Undetected:</b> {domain_report['data']['attributes']['last_analysis_stats']['undetected']}",
                  styles['Normal']))
    story.append(Paragraph("<b>Analysis Results:</b>", styles['Heading2']))

    for engine, result in domain_report['data']['attributes']['last_analysis_results'].items():
        story.append(Paragraph(f"<b>Engine:</b> {engine}<br/><b>Result:</b> {result['result']}", styles['Normal']))

    doc.build(story)


def virustotal_domain_report(domain):
    api_key = '63181217954cb79fe0885566eb5faa561ca74754f02b97d388fa6b6036a90453'
    domain_report_endpoint = f'https://www.virustotal.com/api/v3/domains/{domain}'

    headers = {'x-apikey': api_key}

    response = requests.get(domain_report_endpoint, headers=headers, timeout=10)

    domain_report = response.json()

    if 'data' in domain_report:
        print(Fore.GREEN + "Domain Report:")
        print(f"  - Domain: {domain_report['data']['id']}")
        print(f"  - Last Analysis Date: {domain_report['data']['attributes']['last_analysis_date']}")
        print("   -  Analysis Results:")
        for engine, result in domain_report['data']['attributes']['last_analysis_results'].items():
            print(f"    - Engine: {engine}")
            print(f"      Result: {result['result']}")
        print(f"  - Analysis Status: ")
        print(f"    Harmless: {domain_report['data']['attributes']['last_analysis_stats']['harmless']}")
        print(f"    Malicious: {domain_report['data']['attributes']['last_analysis_stats']['malicious']}")
        print(f"    Suspicious: {domain_report['data']['attributes']['last_analysis_stats']['suspicious']}")
        print(f"    Undetected: {domain_report['data']['attributes']['last_analysis_stats']['undetected']}" + Style.RESET_ALL)

    else:
        print(f"Failed to get domain report. Response: {domain_report}")
    output_directory = 'output'
    output_pdf_file = os.path.join(output_directory, 'VirusTotal_Domain_Report_.pdf')
    create_pdf(domain_report, output_pdf_file)
    print(Fore.RED + f"VirusTotal Report saved to: {output_pdf_file}" + Style.RESET_ALL)

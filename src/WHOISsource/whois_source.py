import whois
import os
from colorama import Fore, Style
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet


def perform_whois_lookup(domain):
    try:
        whois_info = whois.whois(domain)

        print(Fore.RED + "WHOIS information for:", domain)
        print("Registrar:", whois_info.registrar)
        print("Creation Date:", whois_info.creation_date)
        print("Expiration Date:", whois_info.expiration_date)
        print("Nameservers:", whois_info.name_servers)
        print("Org:", whois_info.org)
        print("Email:", whois_info.emails)
        print("Registrant Name:", whois_info.name)
        print("Registrant Address:", whois_info.address)
        print("Registrant City:", whois_info.city)
        print("Registrant State:", whois_info.state)
        print("Registrant Postalcode:", whois_info.registrant_postal_code)
        print("Registrant Country:", whois_info.country)
        print(Style.RESET_ALL)

        create_whois_pdf(whois_info, domain)

    except Exception as e:
        print(f"WHOIS lookup failed: {e}")


def create_whois_pdf(whois_info, domain):
    output_directory = 'output'
    output_pdf_file = os.path.join(output_directory, 'WHOIS_Report.pdf')

    output_dir = os.path.dirname(output_pdf_file)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    doc = SimpleDocTemplate(output_pdf_file, pagesize=letter)
    styles = getSampleStyleSheet()

    story = []

    story.append(Paragraph(f"<b>WHOIS information for:</b> {domain}", styles['Title']))
    story.append(Paragraph(f"<b>Registrar:</b> {whois_info.registrar}", styles['Normal']))
    story.append(Paragraph(f"<b>Creation Date:</b> {whois_info.creation_date}", styles['Normal']))
    story.append(Paragraph(f"<b>Expiration Date:</b> {whois_info.expiration_date}", styles['Normal']))
    story.append(Paragraph(f"<b>Nameservers:</b> {', '.join(whois_info.name_servers)}", styles['Normal']))
    story.append(Paragraph(f"<b>Org:</b> {whois_info.org}", styles['Normal']))
    story.append(Paragraph(f"<b>Email:</b> {', '.join(whois_info.emails)}", styles['Normal']))
    story.append(Paragraph(f"<b>Registrant Name:</b> {whois_info.name}", styles['Normal']))
    story.append(Paragraph(f"<b>Registrant Address:</b> {whois_info.address}", styles['Normal']))
    story.append(Paragraph(f"<b>Registrant City:</b> {whois_info.city}", styles['Normal']))
    story.append(Paragraph(f"<b>Registrant State:</b> {whois_info.state}", styles['Normal']))
    story.append(Paragraph(f"<b>Registrant Postalcode:</b> {whois_info.registrant_postal_code}", styles['Normal']))
    story.append(Paragraph(f"<b>Registrant Country:</b> {whois_info.country}", styles['Normal']))

    doc.build(story)

    print(Fore.RED + f"WHOIS report is saved to: {output_pdf_file}" + Style.RESET_ALL)

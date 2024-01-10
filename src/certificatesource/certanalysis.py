import os
import socket
import ssl
import datetime
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from colorama import Fore, Style

def get_certificate_details(host, port=443):
    try:
        context = ssl.create_default_context()
        with socket.create_connection((host, port)) as sock:
            with context.wrap_socket(sock, server_hostname=host) as ssock:
                cert = ssock.getpeercert()

                subject = dict(item[0] for item in cert['subject'])
                issuer = dict(item[0] for item in cert['issuer'])
                common_name = subject.get('commonName', None)
                not_before = datetime.datetime.strptime(cert['notBefore'], '%b %d %H:%M:%S %Y %Z')
                not_after = datetime.datetime.strptime(cert['notAfter'], '%b %d %H:%M:%S %Y %Z')

                print(Fore.GREEN + f"\nCertificate Information for {host}:{port}")
                print(f"Common Name (CN): {common_name}")
                print(f"Issuer: {issuer['commonName']}")
                print(f"Valid From: {not_before}")
                print(f"Valid Until: {not_after}")
                print(f"Serial Number: {cert['serialNumber']}")
                Style.RESET_ALL
                output_directory = 'output'
                output_pdf_file = os.path.join(output_directory, 'SSL_Certificate_Details.pdf')

                if not os.path.exists(output_directory):
                    os.makedirs(output_directory)

                doc = SimpleDocTemplate(output_pdf_file, pagesize=letter)
                styles = getSampleStyleSheet()

                story = []

                story.append(Paragraph(f"<b>Certificate Information for {host}:{port}</b>", styles['Title']))
                story.append(Paragraph(f"<b>Common Name (CN):</b> {common_name}", styles['Normal']))
                story.append(Paragraph(f"<b>Issuer:</b> {issuer['commonName']}", styles['Normal']))
                story.append(Paragraph(f"<b>Valid From:</b> {not_before}", styles['Normal']))
                story.append(Paragraph(f"<b>Valid Until:</b> {not_after}", styles['Normal']))
                story.append(Paragraph(f"<b>Serial Number:</b> {cert['serialNumber']}", styles['Normal']))

                doc.build(story)

                print(Fore.RED + f"SSL Report saved to: {output_pdf_file}" + Style.RESET_ALL)

    except Exception as e:
        print(f"An error occurred: {e}")

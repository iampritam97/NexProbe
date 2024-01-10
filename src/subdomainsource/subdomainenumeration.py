import os
from src.subdomainsource.crtsh_source import query_crtsh
from tqdm import tqdm
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from colorama import Fore, Style

def enumerate_subdomains(domain):
    crtsh_subdomains = query_crtsh(domain)

    with tqdm(total=len(crtsh_subdomains), unit="Subdomains", desc=f"Enumerating Subdomains for {domain}") as pbar:
        crtsh_subdomains_set = set(crtsh_subdomains)

        subdomains_set = crtsh_subdomains_set

        subdomains = list(subdomains_set)

        for subdomain in subdomains:
            pbar.update(1)

        if subdomains:
            print(Fore.GREEN + f"Subdomains for {domain}:")
            for subdomain in subdomains:
                print(subdomain)
            Style.RESET_ALL
            create_pdf(subdomains, "Subdomains_Report.pdf", domain)

            print(Fore.GREEN + f"Subdomains and PDF report have been generated." + Style.RESET_ALL)
        else:
            print(f"No subdomains found for {domain}.")

    return subdomains


def create_pdf(subdomains, output_file, domain):
    output_directory = 'output'
    output_pdf_file = os.path.join(output_directory, output_file)

    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    pdf = SimpleDocTemplate(output_pdf_file, pagesize=letter)
    story = []

    styles = getSampleStyleSheet()
    story.append(Paragraph("Subdomains Report", styles['Title']))
    story.append(Paragraph(f"Domain: {domain}", styles['Normal']))
    story.append(Spacer(1, 12))

    for subdomain in subdomains:
        story.append(Paragraph(f"Subdomain: {subdomain}", styles['Normal']))

    pdf.build(story)

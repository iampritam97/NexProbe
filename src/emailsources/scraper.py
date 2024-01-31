import os
from bs4 import BeautifulSoup
import re
import threading
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from colorama import Fore, Style
import requests
from urllib.parse import urljoin


email_list_lock = threading.Lock()
email_list = []


def extract_emails_from_text(text):
    return re.findall(r'[\w\.-]+@[\w\.-]+', text, re.IGNORECASE)


def crawl_url(url):
    try:
        if not url.startswith('mailto:'):
            response = requests.get(url)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, 'html.parser')

            emails = extract_emails_from_text(soup.text)

            with email_list_lock:
                email_list.extend(emails)

    except requests.exceptions.RequestException as e:
        print(Fore.RED + f"Error while crawling link: {url}, {e}" + Style.RESET_ALL)


def crawl_domain(domain):
    try:
        base_url = f'https://{domain}'
        response = requests.get(base_url)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')

        links = soup.find_all('a')

        thread_list = []

        for link in links:
            href = link.get('href')

            if href and not href.startswith('mailto:'):
                absolute_url = urljoin(base_url, href)
                thread = threading.Thread(target=crawl_url, args=(absolute_url,))
                thread_list.append(thread)
                thread.start()

        for thread in thread_list:
            thread.join()

    except requests.exceptions.RequestException as e:
        print(Fore.RED + f"Error while crawling domain: {domain}, {e}" + Style.RESET_ALL)


def create_pdf(emails):
    output_directory = 'output'
    output_pdf_file = os.path.join(output_directory, 'Email_Report_Crawl.pdf')

    output_dir = os.path.dirname(output_pdf_file)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    doc = SimpleDocTemplate(output_pdf_file, pagesize=letter)
    styles = getSampleStyleSheet()

    story = []
    title = Paragraph(f"<b>Fetched Emails - Crawler</b>", styles['Title'])
    story.append(title)
    for email in emails:
        story.append(Paragraph(f"<b>Email:</b> {email}", styles['Normal']))

    doc.build(story)

    print(Fore.GREEN + f"PDF report with emails saved to: {output_pdf_file}" + Style.RESET_ALL)


def get_emails_crawl(domain):
    email_list.clear()
    crawl_domain(domain)

    for email in email_list:
        print(Fore.GREEN + email)

    create_pdf(email_list)

    print(Style.RESET_ALL)

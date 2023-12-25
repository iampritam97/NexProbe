import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import urljoin
import threading
from colorama import Fore,Style

email_list_lock = threading.Lock()
email_list = []

def crawl_url(url):
    try:
        response = requests.get(url)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')

        emails = re.findall(r'[\w\.-]+@[\w\.-]+', soup.text)

        with email_list_lock:
            email_list.extend(emails)

    except requests.exceptions.RequestException as e:
        print(f"Error while crawling link: {url}, {e}")

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
        print(f"Error while crawling domain: {domain}, {e}")

def get_emails_from_domain(domain):
    email_list.clear()
    crawl_domain(domain)
    for emails in email_list:
        print(Fore.RED + emails)
    with open("emails.txt", 'w', encoding='utf-8') as file:
        for emails in email_list:
            file.write(emails + '\n')
    print(f"Emails have been saved to emails.txt")
    print(Style.RESET_ALL)

import requests
from bs4 import BeautifulSoup
import re
import time
import random
from urllib.parse import urljoin
import threading

# Create a lock to synchronize access to shared data (email list)
email_list_lock = threading.Lock()
email_list = []

def crawl_url(url):
    try:
        response = requests.get(url)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')

        # Find all the email addresses on the page
        emails = re.findall(r'[\w\.-]+@[\w\.-]+', soup.text)

        # Add found emails to the shared email list
        with email_list_lock:
            email_list.extend(emails)

    except requests.exceptions.RequestException as e:
        print(f"Error while crawling link: {url}, {e}")

def crawl_domain(domain_name):
    try:
        base_url = f'https://{domain_name}'
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

        # Wait for all threads to finish
        for thread in thread_list:
            thread.join()

    except requests.exceptions.RequestException as e:
        print(f"Error while crawling domain: {domain_name}, {e}")

# Get the domain name from the user
domain_name = input("Enter the domain name to find email : ")

# Crawl the domain
crawl_domain(domain_name)

# Print the collected email addresses
with email_list_lock:
    for email in email_list:
        print(email)

import requests
from tqdm import tqdm
from colorama import Fore, Style


def get_urls(domain):
    response = requests.get(f"https://web.archive.org/cdx/search/cdx?url={domain}/*&output=json&fl=original&collapse=urlkey")
    data = response.json()

    urls = [entry[0] for entry in data]

    return urls

def fetch_urls(domain):
    urls = get_urls(domain)
    for url in urls:
        print(Fore.RED + url)
    with tqdm(total=len(urls), unit="URLs", desc="Processing URLs") as pbar:
        with open("urls.txt", 'w', encoding='utf-8') as output_file:
            for url in urls:
                output_file.write(url + '\n')
                pbar.update(1)

    print(f"URLs have been written to urls.txt")
    print(Style.RESET_ALL)

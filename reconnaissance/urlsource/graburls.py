import requests
from tqdm import tqdm  # Import tqdm for the progress bar

def get_urls(domain):
    # Gets URLs from archive.org.
    # Get the JSON response from the archive.org search page for the given domain.
    response = requests.get(f"https://web.archive.org/cdx/search/cdx?url={domain}/*&output=json&fl=original&collapse=urlkey")
    data = response.json()

    # Get URLs from the JSON response.
    urls = [entry[0] for entry in data]

    return urls

def fetch_urls(domain):
    urls = get_urls(domain)
    for url in urls:
        print(url)
    with tqdm(total=len(urls), unit="URLs", desc="Processing URLs") as pbar:
        with open("urls.txt", 'w', encoding='utf-8') as output_file:
            for url in urls:
                output_file.write(url + '\n')
                pbar.update(1)

    print(f"URLs have been written to urls.txt")

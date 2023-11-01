import requests
import re

def query_rapiddns(domain):
    try:
        url = f"https://rapiddns.io/subdomain/{domain}"
        response = requests.get(url)

        if response.status_code == 200:
            subdomains = set(re.findall(r'(?<=<a href="/subdomain/)(.*?)(?=">)', response.text))
            return subdomains
        else:
            return set()
    except Exception as e:
        return set()

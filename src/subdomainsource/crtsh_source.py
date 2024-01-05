import requests
import json


def query_crtsh(domain):
    try:
        url = f"https://crt.sh/?q=%.{domain}&output=json"
        response = requests.get(url)

        if response.status_code == 200:
            data = json.loads(response.text)
            subdomains = set()
            for entry in data:
                subdomains.add(entry['name_value'].strip())
            return list(subdomains)
        else:
            return []
    except Exception as e:
        return []

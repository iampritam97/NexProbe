import requests
import json

def query_alienvault(domain, api_key):
    try:
        url = f"https://otx.alienvault.com:443/api/v1/indicators/domain/{domain}/passive_dns"
        headers = {"X-OTX-API-KEY": api_key}
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            data = response.json()
            subdomains = set()
            for entry in data.get("passive_dns", []):
                subdomains.add(entry["hostname"])
            return subdomains
        else:
            return set()
    except Exception as e:
        return set()

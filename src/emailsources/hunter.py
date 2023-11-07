import requests


def fetch_emails(domain):
    url = "https://api.hunter.io/v2/domain-search"
    headers = {
        "Authorization": f"Bearer YOUR_HUNTER_API_KEY"
    }
    params = {"domain": domain}

    response = requests.get(url, headers=headers, params=params)
    data = response.json() if response.status_code == 200 else {}

    return data.get("data", {}).get("emails", [])

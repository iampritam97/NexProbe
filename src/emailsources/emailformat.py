import requests


def fetch_emails(domain):
    url = "https://api.email-format.com/v1/emails"
    headers = {
        "X-Api-Key": "YOUR_EMAIL_FORMAT_API_KEY"
    }
    params = {"domain": domain}

    response = requests.get(url, headers=headers, params=params)
    data = response.json() if response.status_code == 200 else {}

    return [item["email"] for item in data.get("emails", [])]

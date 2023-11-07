import requests

def fetch_emails(domain, api_key):
    url = "https://api.minelead.io/v1/search/"
    headers = {
        "Authorization": f"Bearer {api_key}"
    }
    params = {
        "domain": domain,
        "max-emails": 4
    }

    response = requests.get(url, headers=headers, params=params)
    data = response.json() if response.status_code == 200 else {}

    return [item["email"] for item in data.get("data", [])]

# Replace 'yourapikey' with your actual API key
api_key = "2d40e947ae04c360db029539afa50cc1"

# Replace 'example.com' with the domain you want to fetch emails for

# Call the function to fetch emails
emails = fetch_emails(domain, api_key)
print(emails)

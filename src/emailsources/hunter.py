import requests

def hunter_fetch_emails(domain):
    api_key = "61150cc37813ef999eba7556f301b88e98b12061"
    url = f"https://api.hunter.io/v2/domain-search?domain={domain}&api_key={api_key}"

    response = requests.get(url)
    data = response.json() if response.status_code == 200 else {}

    emails = data.get("data", {}).get("emails", [])

    for email in emails:
        print(email.get("value"))
    with open("emails.txt", 'a', encoding='utf-8') as file:
        for email in emails:
            file.write(email.get("value") + '\n')
    print(f"Emails have been saved to emails.txt")

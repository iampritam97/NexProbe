import requests
import json


def enumerate_subdomains(domain):
    try:
        # Send a request to the CRT.sh API
        url = f"https://crt.sh/?q=%.{domain}&output=json"
        response = requests.get(url)

        if response.status_code == 200:
            # Parse the JSON response
            data = json.loads(response.text)

            # Extract and format subdomains
            subdomains = set()
            for entry in data:
                subdomains.add(entry['name_value'].strip())

            return subdomains
        else:
            print(f"Failed to fetch subdomains for {domain}.")
            return set()
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return set()

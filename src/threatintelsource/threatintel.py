import requests

# Replace with your AlienVault OTX API key
OTX_API_KEY = "81332555b6860a7b0ef047757fa704037517158e7dedca1494a676866f0d1cfd"

# AlienVault OTX API URL
OTX_API_URL = "https://otx.alienvault.com/api/v1/indicators/domain/{indicator}/{section}"


def query_alienvault_otx(indicator, section="malware"):
    try:
        headers = {"X-OTX-API-KEY": OTX_API_KEY}
        url = OTX_API_URL.format(indicator=indicator, section=section)

        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            data = response.json()
            print(data)
            print("Threat Intelligence Data:")
            for entry in data.get("data", []):
                print(f"Datetime Int: {entry.get('datetime_int', 'N/A')}")
                print(f"Hash: {entry.get('hash', 'N/A')}")
                detections = entry.get('detections', {})
                print("Detections:")
                print(f"  Avast: {detections.get('avast', 'N/A')}")
                print(f"  AVG: {detections.get('avg', 'N/A')}")
                print(f"  ClamAV: {detections.get('clamav', 'N/A')}")
                print(f"  MS Defender: {detections.get('msdefender', 'N/A')}")
                print(f"Date: {entry.get('date', 'N/A')}")
                print()
        else:
            print(f"Failed to retrieve threat intelligence for {indicator}. Status Code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    indicator = input("Enter an indicator (e.g., domain): ")
    query_alienvault_otx(indicator)

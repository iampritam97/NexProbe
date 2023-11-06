import requests
import re
import yaml
from tqdm import tqdm  # Import tqdm for progress bar

# Load the vulnerability patterns from the configuration file
with open("configs/file_exposure_config.yaml", "r") as config_file:
    vulnerabilities = yaml.safe_load(config_file)

def scan_target(target_domain, vulnerabilities):
    try:
        response = requests.get(f"https://{target_domain}")
        if response.status_code == 200:
            with tqdm(total=len(vulnerabilities), desc=f"Scanning {target_domain}") as pbar:
                for vuln in vulnerabilities:
                    name = vuln["name"]
                    pattern = vuln["pattern"]
                    matcher = vuln["matcher"]
                    response2 = requests.get(f"https://{target_domain}{pattern}")
                    if re.search(matcher, response2.text, re.IGNORECASE):
                        print(f"Vulnerability detected on {target_domain}: {name}")
                    # Testing
                    # else:
                    #     print(f"{target_domain}/{pattern}")
                    pbar.update(1)  # Update the progress bar
    except requests.exceptions.RequestException as e:
        print(f"Error scanning {target_domain}: {e}")

def main():
    target_domain = input("Enter the target domain (e.g., example.com): ")
    scan_target(target_domain, vulnerabilities)

if __name__ == "__main__":
    main()

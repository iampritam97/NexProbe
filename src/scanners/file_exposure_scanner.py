import os
from colorama import Fore, Style
import requests
import re
import yaml
from tqdm import tqdm

script_directory = os.path.dirname(os.path.realpath(__file__))
config_file_path = os.path.join(script_directory, "configs", "file_exposure_config.yaml")
with open(config_file_path, "r") as config_file:
    vulnerabilities = yaml.safe_load(config_file)

def file_exposure(target_domain):
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
                        print(Fore.RED + f"File exposure detected on {target_domain}{pattern}: {name}")
                        print(Style.RESET_ALL)
                    pbar.update(1)
    except requests.exceptions.RequestException as e:
        print(f"Error scanning {target_domain}: {e}")



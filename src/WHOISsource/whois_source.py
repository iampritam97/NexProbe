import whois
from colorama import Fore, Back, Style

def perform_whois_lookup(domain):

    try:
        whois_info = whois.whois(domain)
        print(Fore.RED + "WHOIS information for:", domain)
        print("Registrar:", whois_info.registrar)
        print("Creation Date:", whois_info.creation_date)
        print("Expiration Date:", whois_info.expiration_date)
        print("Nameservers:", whois_info.name_servers)
        print("Org:", whois_info.org)
        print("Email:", whois_info.emails)
        print("Registrant Name:", whois_info.name)
        print("Registrant Address:", whois_info.address)
        print("Registrant City:", whois_info.city)
        print("Registrant State:", whois_info.state)
        print("Registrant Postalcode:", whois_info.registrant_postal_code)
        print("Registrant Country:", whois_info.country)
        print(Style.RESET_ALL)
    except Exception as e:
        print(f"WHOIS lookup failed: {e}")
import argparse
import subprocess
from colorama import Fore
from src.WHOISsource.whois_source import perform_whois_lookup
from src.scanners.xss_scanner import xss
from src.subdomainsource.subdomainenumeration import enumerate_subdomains
from src.certificatesource.certanalysis import get_certificate_details_from_main
from src.emailsources.scraper import get_emails_from_domain
from src.emailsources.hunter import hunter_fetch_emails
from src.urlsource.graburls import fetch_urls
from src.scanners.file_exposure_scanner import file_exposure
from src.scanners.HeaderAnalyse import scan_headers


def active_reconnaissance(domain):
    scan_headers(domain)
    xss(domain)
    get_emails_from_domain(domain)
    hunter_fetch_emails(domain)
    file_exposure(domain)

def passive_reconnaissance(domain):
    enumerate_subdomains(domain)
    get_certificate_details_from_main(domain)
    perform_whois_lookup(domain)
    fetch_urls(domain)


def update_tool():
    print("Updating NexProbe.........")

    try:
        subprocess.run(["git", "pull", "origin", "main"])
        print("Update successful.")
    except Exception as e:
        print(f"Update failed: {e}")

def main():
    print(Fore.CYAN + r"""
     █████╗ ██╗███████╗██╗  ██╗██████╗ ██████╗  ██████╗ ██████╗ ███████╗
     █████╗ ██║██╔════╝╚██╗██╔╝██╔══██╗██╔══██╗██╔═══██╗██╔══██╗██╔════╝
     ██╔██╗ ██║█████╗   ╚███╔╝ ██████╔╝██████╔╝██║   ██║██████╔╝█████╗  
     ██║╚██╗██║██╔══╝   ██╔██╗ ██╔═══╝ ██╔══██╗██║   ██║██╔══██╗██╔══╝  
     ██║ ╚████║███████╗██╔╝ ██╗██║     ██║  ██║╚██████╔╝██████╔╝███████╗
     ╚═╝  ╚═══╝╚══════╝╚═╝  ╚═╝╚═╝     ╚═╝  ╚═╝ ╚═════╝ ╚═════╝ ╚══════╝
                        """)
    parser = argparse.ArgumentParser(description="Reconnaissance tool for active and passive scanning of domains.")
    parser.add_argument("-p", "--passive", action="store_true", help="Perform Passive Reconnaissance")
    parser.add_argument("-a", "--active", action="store_true", help="Perform Active Reconnaissance")
    parser.add_argument("-d", "--domain", type=str, help="Target domain (e.g., example.com)")
    parser.add_argument("--update", action="store_true", help="Update the tool")
    args = parser.parse_args()

    if args.update:
        update_tool()
    else:
        if args.passive and args.active:
            print("Please choose either passive (-p) or active (-a) reconnaissance, not both.")
        elif args.passive:
            domain = args.domain or input("Enter the target domain (e.g., example.com): ")
            passive_reconnaissance(domain)
        elif args.active:
            domain = args.domain or input("Enter the target domain (e.g., example.com): ")
            active_reconnaissance(domain)
        else:
            print("Please specify either passive (-p) or active (-a) reconnaissance.")

if __name__ == "__main__":
    main()

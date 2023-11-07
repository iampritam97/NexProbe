from src.WHOISsource.whois_source import perform_whois_lookup
from src.scanners.xss_scanner import xss
from src.subdomainsource.subdomainenumeration import enumerate_subdomains
from src.certificatesource.certanalysis import get_certificate_details_from_main
from src.emailsources.scraper import get_emails_from_domain
from src.urlsource.graburls import fetch_urls
def main():
    print(r"""\
███╗   ██╗███████╗██╗  ██╗██████╗ ██████╗  ██████╗ ██████╗ ███████╗
████╗  ██║██╔════╝╚██╗██╔╝██╔══██╗██╔══██╗██╔═══██╗██╔══██╗██╔════╝
██╔██╗ ██║█████╗   ╚███╔╝ ██████╔╝██████╔╝██║   ██║██████╔╝█████╗  
██║╚██╗██║██╔══╝   ██╔██╗ ██╔═══╝ ██╔══██╗██║   ██║██╔══██╗██╔══╝  
██║ ╚████║███████╗██╔╝ ██╗██║     ██║  ██║╚██████╔╝██████╔╝███████╗
╚═╝  ╚═══╝╚══════╝╚═╝  ╚═╝╚═╝     ╚═╝  ╚═╝ ╚═════╝ ╚═════╝ ╚══════╝
                    """)
    while True:
        print("\nChoose your reconnaissance method:")
        print("1. Active Reconnaissance")
        print("2. Passive Reconnaissance")
        print("3. Exit")
        choice = input("Enter your choice (1/2/3): ")

        if choice == "1":
            domain = input("Enter the target domain (e.g., example.com): ")
            xss(domain)
            get_emails_from_domain(domain)


        elif choice == "2":
            domain = input("Enter the target domain (e.g., example.com): ")
            enumerate_subdomains(domain)
            get_certificate_details_from_main(domain)
            perform_whois_lookup(domain)
            fetch_urls(domain)

        elif choice == "3":
            print("Goodbye!")
            break

if __name__ == "__main__":
    main()

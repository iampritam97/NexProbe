from reconnaissance.WHOISsource.whois_source import perform_whois_lookup

if __name__ == "__main__":
    domain_name = input("Enter the domain name for WHOIS lookup: ")
    result = perform_whois_lookup(domain_name)

    print("WHOIS Information:")
    print(result)
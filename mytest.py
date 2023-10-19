from reconnaissance.subdomainenumeration import enumerate_subdomains

domain = "bing.com"
subdomains = enumerate_subdomains(domain)

if subdomains:
    print(f"Subdomains for {domain}:")
    for subdomain in subdomains:
        print(subdomain)
else:
    print(f"No subdomains found for {domain}.")

from reconnaissance.subdomainsource.crtsh_source import query_crtsh
from tqdm import tqdm

def enumerate_subdomains(domain):
    crtsh_subdomains = query_crtsh(domain)

    # Use tqdm to create a progress bar
    with tqdm(total=len(crtsh_subdomains), unit="Subdomains", desc=f"Enumerating Subdomains for {domain}") as pbar:
        crtsh_subdomains_set = set(crtsh_subdomains)

        subdomains_set = crtsh_subdomains_set

        subdomains = list(subdomains_set)

        for subdomain in subdomains:
            pbar.update(1)  # Update the progress bar

        if subdomains:
            print(f"Subdomains for {domain}:")
            for subdomain in subdomains:
                print(subdomain)
            # Write subdomains to the specified output file
            with open("subdomains.txt", 'w', encoding='utf-8') as file:
                for subdomain in subdomains:
                        file.write(subdomain + '\n')

            print(f"Subdomains have been saved to subdomains.txt")
        else:
            print(f"No subdomains found for {domain}.")
    return subdomains

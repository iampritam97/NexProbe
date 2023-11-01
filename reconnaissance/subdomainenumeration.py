from reconnaissance.subdomainsource.crtsh_source import query_crtsh
from reconnaissance.subdomainsource.alienvault_source import query_alienvault
from reconnaissance.subdomainsource.rapiddns_source import query_rapiddns

def enumerate_subdomains(domain, alienvault_api_key=None):
    crtsh_subdomains = query_crtsh(domain)
    alienvault_subdomains = set()
    rapiddns_subdomains = query_rapiddns(domain)

    if alienvault_api_key:
        alienvault_subdomains = query_alienvault(domain, alienvault_api_key)

    subdomains = crtsh_subdomains.union(alienvault_subdomains).union(rapiddns_subdomains)
    return subdomains

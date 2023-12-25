import ssl
import socket
import datetime
from colorama import Fore, Style

def get_certificate_details(host, port=443):
    try:
        context = ssl.create_default_context()
        with socket.create_connection((host, port)) as sock:
            with context.wrap_socket(sock, server_hostname=host) as ssock:
                cert = ssock.getpeercert()

                subject = dict(item[0] for item in cert['subject'])
                issuer = dict(item[0] for item in cert['issuer'])
                common_name = subject.get('commonName', None)
                not_before = datetime.datetime.strptime(cert['notBefore'], '%b %d %H:%M:%S %Y %Z')
                not_after = datetime.datetime.strptime(cert['notAfter'], '%b %d %H:%M:%S %Y %Z')

                print(Fore.RED + f"Certificate Information for {host}:{port}")
                print(f"Common Name (CN): {common_name}")
                print(f"Issuer: {issuer['commonName']}")
                print(f"Valid From: {not_before}")
                print(f"Valid Until: {not_after}")
                print(f"Serial Number: {cert['serialNumber']}")
                print(Style.RESET_ALL)
    except Exception as e:
        print(f"An error occurred: {e}")

def get_certificate_details_from_main(domain):
    host = domain
    get_certificate_details(host)
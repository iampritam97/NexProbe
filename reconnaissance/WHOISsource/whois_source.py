import socket


def perform_whois_lookup(domain_name):
    whois_server = "whois.iana.org"

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((whois_server, 43))
            s.send(f"{domain_name}\r\n".encode())

            response = b""
            while True:
                data = s.recv(4096)
                if not data:
                    break
                response += data

            return response.decode("utf-8")
    except Exception as e:
        return str(e)

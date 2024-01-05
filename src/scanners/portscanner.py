import os
import socket
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from colorama import Fore, Style


def port_scan(host, port):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(1)
            result = sock.connect_ex((host, port))

            if result == 0:
                print(Fore.RED + f"Port {port} on {host} is open" + Style.RESET_ALL)
                return True
            else:
                print(f"Port {port} on {host} is closed")
                return False

    except socket.error as e:
        print(f"Error scanning port {port} on {host}: {e}")
        return False


def multi_port_scan(host, ports):
    open_ports = [port for port in ports if port_scan(host, port)]
    return open_ports


def portscan_main(domain):
    predefined_ports = [20, 21, 22, 23, 25, 53, 137, 139, 445, 80, 443, 8080, 8443, 1433, 1434, 3306,
                        3389]

    open_ports = multi_port_scan(domain, predefined_ports)

    if open_ports:
        print(Fore.RED + f"Open ports on {domain}: {open_ports}" + Style.RESET_ALL)

        create_pdf(open_ports, domain)

    else:
        print(f"No open ports found on {domain}")


def create_pdf(open_ports, domain):
    output_directory = 'output'
    output_pdf_file = os.path.join(output_directory, 'Port_Scan_Report.pdf')

    output_dir = os.path.dirname(output_pdf_file)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    doc = SimpleDocTemplate(output_pdf_file, pagesize=letter)
    styles = getSampleStyleSheet()

    story = []
    title = Paragraph(f"<b>Port Scanning for {domain}</b>", styles['Title'])
    story.append(title)
    story.append(Paragraph(f"<b>Open Ports:</b> {', '.join(map(str, open_ports))}", styles['Normal']))

    doc.build(story)

    print(f"PDF report with open ports saved to: {output_pdf_file}")

import os
import requests
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

def query_urlhaus(url):
    # Construct the HTTP request
    data = {'host': url}
    response = requests.post('https://urlhaus-api.abuse.ch/v1/host/', data)

    # Parse the response from the API
    json_response = response.json()
    # Output directory and filename
    output_directory = 'output'
    output_pdf_file = os.path.join(output_directory, 'URLhaus_Domain_Report_.pdf')

    # Check if the output directory exists and create it if not
    output_dir = os.path.dirname(output_pdf_file)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Create a PDF document using SimpleDocTemplate
    doc = SimpleDocTemplate(output_pdf_file, pagesize=letter)
    styles = getSampleStyleSheet()

    # Story to hold the content
    story = []

    # Add title to the PDF
    title = Paragraph(f"<b>URLhaus Result - {url}</b>", styles['Title'])
    story.append(title)

    # Add content to the PDF
    story.append(Paragraph(f"<b>Query Status:</b> {json_response['query_status']}", styles['Normal']))

    if json_response['query_status'] == 'ok':
        print(f"URLhaus Query Result for {url} :")
        for results in json_response['urls']:
            print(f"URL: {results['url']}")
            print(f"Tags: {results['tags']}")
            print(f"Threat: {results['threat']}")
            print(f"Date Added: {results['date_added']}")
            print(f"Current Status: {results['url_status']}")

        # Add query results to the PDF
        for result in json_response['urls']:
            story.append(Paragraph(f"<b>URL:</b> {result['url']}", styles['Normal']))
            story.append(Paragraph(f"<b>Tags:</b> {', '.join(result['tags'])}", styles['Normal']))
            story.append(Paragraph(f"<b>Threat:</b> {result['threat']}", styles['Normal']))
            story.append(Paragraph(f"<b>Date Added:</b> {result['date_added']}", styles['Normal']))
            story.append(Paragraph(f"<b>Current Status:</b> {result['url_status']}", styles['Normal']))
            story.append(Paragraph("<br/>", styles['Normal']))

    # Build the PDF document
    doc.build(story)

    print(f"Report saved to: {output_pdf_file}")


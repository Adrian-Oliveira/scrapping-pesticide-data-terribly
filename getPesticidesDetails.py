import  re 
import requests
from pdfminer.high_level import extract_pages, extract_text
import tabula
import io


#pdf_url = "https://www.gov.br/anvisa/pt-br/setorregulado/regularizacao/agrotoxicos/monografias/monografias-autorizadas/a/acefato"
pdf_url = "https://www.gov.br/anvisa/pt-br/setorregulado/regularizacao/agrotoxicos/monografias/monografias-autorizadas/a/4154json-file-1"
# Send a GET request to download the PDF
response = requests.get(pdf_url)

# Check if the request was successful
if response.status_code == 200:
    # Create a BytesIO object from the response content
    pdf_file = io.BytesIO(response.content)

    # Use pdfminer to extract text from the PDF
    text = extract_text(pdf_file)

    # Print the extracted text
    print(text)
else:
    print(f"Failed to download PDF. Status code: {response.status_code}")



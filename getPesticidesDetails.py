import  re 
import requests
from pdfminer.high_level import extract_pages, extract_text
import tabula
import io

def extract_data(text):
    data = {}
    pattern = r'([^(]+)\s*$\s*([^)]+)\s*$'
    
    # Find all matches in the text
    matches = re.findall(pattern, text)

    # Process and print the results
    for match in matches:
        before_parenthesis = match[0].strip()  # Value before the last parenthesis
        inside_parenthesis = match[1].strip()   # Value inside the last parenthesis
        print(f"Before Parenthesis: {before_parenthesis}")
        print(f"Inside Parenthesis: {inside_parenthesis}")


    # Regular expressions to match the required fields

    patterns = {
        'ingrediente_ativo': r'a\) Ingrediente ativo ou nome comum:\s*(.*)',
        'número_CAS': r'c\) N° CAS:\s*(.*)',
        'nome_químico': r'd\) Nome químico:\s*(.*)',
        'fórmula_bruta': r'e\) Fórmula bruta:\s*(.*)',
        'grupo_químico': r'g\) Grupo químico:\s*(.*)',
        'classe': r'h\) Classe:\s*(.*)'
    }
    
    # Extract data using the defined patterns
    for key, pattern in patterns.items():
        match = re.search(pattern, text)
        print(match)
        if match:
            data[key] = match.group(1).strip()  # Get the matched group and strip whitespace
    
    return data



pdf_url = "https://www.gov.br/anvisa/pt-br/setorregulado/regularizacao/agrotoxicos/monografias/monografias-autorizadas/a/4154json-file-1"
pdf_url = "https://www.gov.br/anvisa/pt-br/setorregulado/regularizacao/agrotoxicos/monografias/monografias-autorizadas/a/acefato"
# Send a GET request to download the PDF
print('buscando dados')
response = requests.get(pdf_url)

# Check if the request was successful
if response.status_code == 200:
    # Create a BytesIO object from the response content
    pdf_file = io.BytesIO(response.content)

    # Use pdfminer to extract text from the PDF
    text = extract_text(pdf_file)

    extracted_data = extract_data(text)

    for key, value in extracted_data.items():
        print(value) if value[-1] == ')' else None
        print(f"{key.replace('_', ' ').title()}: {value}")

else:
    print(f"Failed to download PDF. Status code: {response.status_code}")



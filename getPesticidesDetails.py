import  re 
import requests
from pdfminer.high_level import extract_pages, extract_text
import tabula
import io
import json
import csv


def extract_name_Ptbr_and_En(text:str)-> list[str]:
    l, r = 0, len(text) - 1

    while r >= 0 and text[r] != ')':
        r -= 1
    print(text)
    print(r)
    if r <= 0:
        return [text, text]
    else:
        l = r 
        countOpenParentheses = 1
        while countOpenParentheses and l>0:
            l -= 1
            if text[l] == ')':
                countOpenParentheses += 1
            if text[l] == '(':
                countOpenParentheses -= 1

        #      [PtBrName, EnName]
        return [text[:l], text[l+1:r]]
 
def extract_data(text):
    data = {}
    pattern = r'(?:comum|ativo):(.*?)(?=b\))'
    # Search for the pattern in the text    
    match = re.search(pattern, text, re.DOTALL) 

    if match:
        result = match.group(1).strip()  # Get the captured group and strip whitespace
        ptBrName, EnName = extract_name_Ptbr_and_En(result)
        data['ptBrName'] = ptBrName.strip()
        data['enName'] = EnName.strip()
    else:
        print("No match found.")


    # Regular expressions to match the required fields
    #'ingrediente_ativo': r'a\) Ingrediente ativo ou nome comum:\s*(.*)',
    #'número_CAS': r'c\) N° CAS:\s*(.*)', 

    patterns = {
        'nome_químico': r'd\) Nome químico:\s*(.*)',
        'fórmula_bruta': r'e\) Fórmula bruta:\s*(.*)',
        'grupo_químico': r'g\) Grupo químico:\s*(.*)',
        'classe': r'h\) Classe:\s*(.*)'
    }
    
    # Extract data using the defined patterns
    for key, pattern in patterns.items():
        match = re.search(pattern, text)
        if match:
            data[key] = match.group(1).strip()  # Get the matched group and strip whitespace
    
    return data



#pdf_url = "https://www.gov.br/anvisa/pt-br/setorregulado/regularizacao/agrotoxicos/monografias/monografias-autorizadas/a/4154json-file-1"
#pdf_url = "https://www.gov.br/anvisa/pt-br/setorregulado/regularizacao/agrotoxicos/monografias/monografias-autorizadas/a/acefato"
arr = [
    "https://www.gov.br/anvisa/pt-br/setorregulado/regularizacao/agrotoxicos/monografias/monografias-autorizadas/a/4154json-file-1",
    "https://www.gov.br/anvisa/pt-br/setorregulado/regularizacao/agrotoxicos/monografias/monografias-autorizadas/a/acefato",
    "https://www.gov.br/anvisa/pt-br/setorregulado/regularizacao/agrotoxicos/monografias/monografias-autorizadas/a/4176json-file-1",
    "https://www.gov.br/anvisa/pt-br/setorregulado/regularizacao/agrotoxicos/monografias/monografias-autorizadas/a/4177json-file-1"
]




with open('db.json','w') as f, open('pesticidasPermitidosRevisado.csv', 'r') as f2:
    db = {}
    reader = csv.reader(f2)
    next(reader)  # Skip the first row

    for pesticide in reader:
        
        # Send a GET request to download the PDF
        print('fetching data ...')
        print(pesticide[0])
        response = requests.get(pesticide[1])
        
        #response = requests.get(pesticide)

        # Check if the request was successful
        if response.status_code == 200:
            # Create a BytesIO object from the response content
            pdf_file = io.BytesIO(response.content)

            # Use pdfminer to extract text from the PDF
            text = extract_text(pdf_file)

            extracted_data = extract_data(text)
            
            if 'ptBrName' in extracted_data:
                db[extracted_data['ptBrName']] = extracted_data
            
        else:
            print(f"Failed: {pesticide[1]}")
    
    json.dump(db, f, indent=4)


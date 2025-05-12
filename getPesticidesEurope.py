import json
import requests

# Load the JSON file
with open('db.json', 'r') as file:
    data = json.load(file)

# Iterate through the list of substance objects
for substance in data:
    
    substance_name = data[substance]['enName']  # Adjust this based on your JSON structure
    data[substance]['aprovadoEm'] = ['Brasil']
    if substance_name:  # Ensure the substance_name is not None
        api_url = f"https://api.datalake.sante.service.ec.europa.eu/sante/pesticides/active_substances?format=json&substance_name={substance_name}%20acid&api-version=v2.0"
        
        # Make the GET request
        response = requests.get(api_url)
        
        if response.status_code == 200:
            response_data = response.json()
            
            # Initialize the approvedId array for the current substance
            
            # Check if the response has the expected structure
            if 'value' in response_data and len(response_data['value']) > 0:
                if response_data['value'][0].get('substance_status') == "Approved":
                    # Add "Europa" to the approvedId array for the current substance
                    data[substance]['aprovadoEm'].append("Europa")
        else:
            print(substance_name)
    

# Write the modified data back to the JSON file
with open('dbBR_EU.json', 'w') as file:
    json.dump(data, file, indent=4)

print("Process completed successfully.")
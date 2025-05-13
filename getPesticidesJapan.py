import json

with open('dbBR_EU.json', 'r') as file:
    data = json.load(file)



pesticidesInJapan = set()
# Open the file and read its contents
with open('./pesticidesJapan.txt', 'r') as pesticidesInJapanFile:

    for pesticides in pesticidesInJapanFile:
        # Strip whitespace and add to the set
        pesticidesInJapan.add(pesticides.strip().lower())


# Print the resulting set
#print(pesticidesInJapan)

for pesticide in data:
    print(pesticide)
    print(data[pesticide]['enName'])
    if data[pesticide]['enName'].lower() in pesticidesInJapan:
        data[pesticide]['aprovadoEm'].append('Japão')



# Write the modified data back to the JSON file
with open('db_BR_EU_JP.json', 'w') as file:
    json.dump(data, file, indent=4)

print("Process completed successfully.")
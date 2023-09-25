import pandas as pd
import numpy as np
import random

excelsheet = pd.read_excel('Running Dinner dataset 2022.xlsx', sheet_name='Bewoners') 
excelsheet2 = pd.read_excel('Running Dinner dataset 2022.xlsx', sheet_name='Adressen')
df = pd.DataFrame(excelsheet)
df2 = pd.DataFrame(excelsheet2)
df = df.drop(columns='Kookt niet')
df2 = df2.drop(columns='Voorkeur gang')
df = df.merge(df2, how='left', on='Huisadres')
df.fillna(0, inplace=True)

# Aantal gangen, nodig voor the for loop.
aantal_gangen = 3
# Namen van de gangen.
gang = ['Voorgerecht', 'Hoofdgerecht', 'Nagerecht']

# Create a list of all unique house addresses
all_houses = df['Huisadres'].unique()

# Initialize the gangen dictionary with empty lists for all house addresses
gangen = {house: [] for house in all_houses}

# Create a list of available individuals
available_individuals = df['Bewoner'].tolist()
print(len(available_individuals))
# For loop where gang_num and gang_naam are taken from the gang list (3 loops).
for gang_num, gang_naam in enumerate(gang):
    dfMensInfo = df.sample(frac=1, random_state=42)
    max_grootteHuizen = dfMensInfo['Max groepsgrootte']
    min_grootteHuizen = dfMensInfo['Min groepsgrootte']

    # Iterate over all house addresses
    for i, house in enumerate(all_houses):
        max_huisgrootte = int(max_grootteHuizen[i])
        min_huisgrootte = int(min_grootteHuizen[i])

        # Ensure that max_huisgrootte is at least equal to min_huisgrootte
        max_huisgrootte = max(max_huisgrootte, min_huisgrootte)

        if max_huisgrootte > 0 and len(available_individuals) >= max_huisgrootte:
            random_persons = random.sample(available_individuals, max_huisgrootte)
        else:
            random_persons = []

        gangen[house].extend(random_persons)
        available_individuals = [ind for ind in available_individuals if ind not in random_persons]



for huis, personen in gangen.items():
    # Print the house and assigned individuals
    print(f"{huis}: {personen}")


# ... (Previous code)

# Initialize a list to keep track of all assigned individuals
all_assigned_individuals = []

# Initialize the gangen dictionary as an empty dictionary for each house
gangen = {house: {} for house in all_houses}

# For loop where gang_num and gang_naam are taken from the gang list (3 loops).
for gang_num, gang_naam in enumerate(gang):
    dfMensInfo = df.sample(frac=1, random_state=42)
    max_grootteHuizen = dfMensInfo['Max groepsgrootte']
    min_grootteHuizen = dfMensInfo['Min groepsgrootte']

    # Iterate over all house addresses
    for i, house in enumerate(all_houses):
        max_huisgrootte = int(max_grootteHuizen[i])
        min_huisgrootte = int(min_grootteHuizen[i])

        # Ensure that max_huisgrootte is at least equal to min_huisgrootte
        max_huisgrootte = max(max_huisgrootte, min_huisgrootte)

        if max_huisgrootte > 0 and len(available_individuals) >= max_huisgrootte:
            random_persons = random.sample(available_individuals, max_huisgrootte)
        else:
            random_persons = []

        # Check if the gang key exists for this house, and if not, create it
        if gang_naam not in gangen[house]:
            gangen[house][gang_naam] = []

        gangen[house][gang_naam].extend(random_persons)
        available_individuals = [ind for ind in available_individuals if ind not in random_persons]

        # Add assigned individuals to the list of all assigned individuals
        all_assigned_individuals.extend(random_persons)

# ... (Previous code)

# Assign any remaining individuals randomly to houses
while available_individuals:
    random_house = random.choice(all_houses)
    random_person = available_individuals.pop()
    
    # Extract the Max groepsgrootte value for the selected house
    max_grootte_huis = dfMensInfo[dfMensInfo['Huisadres'] == random_house]['Max groepsgrootte'].iloc[0]
    
    # Iterate over gangen for the selected house and assign the individual
    for gang_naam in gang:
        if len(gangen[random_house][gang_naam]) < int(max_grootte_huis):
            gangen[random_house][gang_naam].append(random_person)
            all_assigned_individuals.append(random_person)

# Check if all available individuals have been assigned
if set(all_assigned_individuals) == set(df['Bewoner']):
    print("All available individuals have been assigned.")
else:
    print("Not all available individuals have been assigned.")

# Rest of your code



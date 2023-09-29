import pandas as pd
import random

# Read the Excel files into DataFrames
excelsheet = pd.read_excel('Running Dinner dataset 2022.xlsx', sheet_name='Bewoners') 
excelsheet2 = pd.read_excel('Running Dinner dataset 2022.xlsx', sheet_name='Adressen')

# Create DataFrames from the Excel sheets
df = excelsheet.drop(columns='Kookt niet')
df2 = excelsheet2.drop(columns='Voorkeur gang')

# Merge the DataFrames on 'Huisadres'
df = df.merge(df2, how='left', on='Huisadres')

# Fill NaN values with 0
df.fillna(0, inplace=True)

# Define constants
aantal_gangen = 3
gang = ['Voorgerecht', 'Hoofdgerecht', 'Nagerecht']

# Create a list of all unique house addresses
all_houses = df['Huisadres'].unique()

# Initialize a dictionary to track each person's assigned houses
person_assignments = {}

# Create a list of available individuals
available_individuals = df['Bewoner'].tolist()

# For loop to assign houses to persons
for gang_naam in gang:
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

        available_individuals = [ind for ind in available_individuals if ind not in random_persons]

        # Update the person_assignments dictionary for the current gang
        for person in random_persons:
            if person not in person_assignments:
                person_assignments[person] = {
                    'Own_House': house,
                    gang_naam: house,
                }
            else:
                person_assignments[person][gang_naam] = house

# Create a structured DataFrame
structured_data = []

for person, assignments in person_assignments.items():
    structured_data.append(assignments)

structured_df = pd.DataFrame(structured_data)

# Save the resulting DataFrame to an Excel file
structured_df.to_excel('testmetsam.xlsx', index=False)

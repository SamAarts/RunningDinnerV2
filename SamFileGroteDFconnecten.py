import pandas as pd
import numpy as np
import random


excelsheet = pd.read_excel('Running Dinner dataset 2022.xlsx', sheet_name='Bewoners') 
excelsheet2 = pd.read_excel('Running Dinner dataset 2022.xlsx', sheet_name='Adressen')
df = pd.DataFrame(excelsheet)
df2 = pd.DataFrame(excelsheet2)
df = df.drop(columns='Kookt niet')
df2 = df2.drop(columns='Voorkeur gang')


Mensen = list(df['Bewoner'])
Huizen = list(df['Huisadres'])

df = df.merge(df2, how = 'left', on ='Huisadres')
df.fillna(0, inplace=True)



max_grootteHuizen = df['Max groepsgrootte']
min_grootteHuizen = df['Min groepsgrootte']

# We maken dataframes van deze lijsten om makkelijker te kunnen rekenen.
dfMensen = pd.DataFrame(Mensen, columns=['Mensen'])
dfHuizen = pd.DataFrame(Huizen, columns=['Huizen'])
# Aantal gangen, nodig voor de for loop.
aantal_gangen = 3
# Maak een dictonairy van gangen.
gangen = [{} for _ in range(aantal_gangen)]
# Namen van de gangen.
gang = ['Voorgerecht', 'Hoofdgerecht', 'Nagerecht']



# Forloop waarin de gang_num en de gang_naam als variabele worden meegenomen in de lengte van gang (3 dus).
for gang_num, gang_naam in enumerate(gang):
    # Maak een lijst van beschikbare individuen. Deze zetten we in de for loop omdat voor elke gang alle mensen weer verdeeld moeten worden.
    available_individuals = dfMensen['Mensen'].tolist()

    # Maakt een for loop van de lengte van alle huizen.
    for i in range(len(Huizen)):
        # Maakt een variabele aan hoeveel mensen er in een huis passen.
        max_huisgrootte = int(max_grootteHuizen[i])
        min_huisgrootte = int(min_grootteHuizen[i])
        
        # Controleer of er genoeg individuen over zijn om uit te kiezen
        if len(available_individuals) < min_huisgrootte:
            break  # Niet genoeg unieke individuen om te selecteren
        
        # Ensure that max_huisgrootte is at least equal to min_huisgrootte
        max_huisgrootte = max(max_huisgrootte, min_huisgrootte)
        
        # Here, it takes a number of max_huisgrootte from huis i and selects them randomly from available_individuals.
        random_persons = random.sample(available_individuals, max_huisgrootte)
        # Here, we create a new list in the dictionary using the house key for the selected individuals.
        gangen[gang_num][Huizen[i]] = random_persons       

        # Here, all "used" individuals are removed from the list to start the next iteration of the for loop with a smaller list of individuals.
        available_individuals = [ind for ind in available_individuals if ind not in random_persons]


# Weer loopen over 2 variabele
for gang_num, gang_dict in enumerate(gangen):
    # Hier printen we de gang
    print(f"Gang {gang[gang_num]}:")
    # Hier loopen we over elk huis
    for huis, personen in gang_dict.items():
        # Hier printen we de mensen in elk huis
        print(f"{huis}: {personen}")

print()
print()
print(personen)
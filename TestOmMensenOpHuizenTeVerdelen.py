import random
import numpy as np
import pandas as pd


# Eerst maken we een lijst met alle mensen die mee doen aan het diner
Mensen = ["M_1", "V_1", "M_2", "V_2", "M_3", "V_3", "M_4", "V_4", "M_5", "V_5"]
# Dan maken we een lijst met alle huizen die beschikbaar zijn voor het diner
Huizen = ['H_1', 'H_2', 'H_3', 'H_4', 'H_5']
# Op hetzelfde index maken we een lijst hoeveel gasten het huis maximaal kan hebben.
grootteHuizen = [3, 2, 0, 3, 2]
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
    # Maak een lijst van beschikbare individuen. Deze zetten we in de for loop omdat voor elke gang allemensen weer verdeeld moeten worden.
    available_individuals = dfMensen['Mensen'].tolist()

    # Maakt een for loop van de lengte van alle huizen.
    for i in range(len(Huizen)):
        # Maakt een variabele aan hoeveel mensen er in een huis passen.
        huisgrootte = grootteHuizen[i]
        
        # Controleer of er genoeg individuen over zijn om uit te kiezen
        if len(available_individuals) < huisgrootte:
            break  # Niet genoeg unieke individuen om te selecteren
            
        #Hier neemt hij een aantal huisgrootte van huis i, en haalt hij random uit available_individuals. 
        random_persons = random.sample(available_individuals, huisgrootte)
        # Hier maken we van de geselecteerde mensen, met behulpt van de huis key een nieuwe lijst in de dictonairy.
        gangen[gang_num][Huizen[i]] = random_persons       

        # Hier worden alle "Gebruikte" mensen uit de lijst gehaald om de volgede itteratie van de forloop met een kleinere lijst met mensen te beginnen.
        available_individuals = [ind for ind in available_individuals if ind not in random_persons]

# Weer loopen over 2 variabele
for gang_num, gang_dict in enumerate(gangen):
    # Hier printen we de gang
    print(f"Gang {gang[gang_num]}:")
    # Hier loopen we over elk huis
    for huis, personen in gang_dict.items():
        # Hier printen we de mensen in elk huis
        print(f"{huis}: {personen}")


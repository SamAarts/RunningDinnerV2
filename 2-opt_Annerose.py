# Eerst importeren we alle benodigde libraries.
import random
import logging
import pandas as pd
import itertools
import matplotlib.pyplot as plt
import importlib #Dit is een library die ervoor zorgt dat het importeren van functies soepeler verloopt. 
                 #Er is een kans dat het geheugen niet meelaad met de veranderingen van de dataframes, dit voorkomt dat.
import sys
from collections import defaultdict
sys.path.append('code/')
# Hieronder importeren we onze eigengeschreven functies.
from Wensen_planning import * 
from Eisen_planning import *

# Hier roepen we onze log aan, in dit document kunnen we de veranderingen overzichtelijk zien van onze 2opt.
logger = logging.getLogger(name='2opt-logger')
logging.basicConfig(level=logging.DEBUG,
                    format='[%(asctime)s] %(message)s',
                    handlers=[logging.FileHandler("2-opt_debug-Sam.log")])

# Dit is de functie die zorgt dat onze functies blijven opnieuw inladen.
importlib.reload(sys.modules['Wensen_planning'])

# Hier maken we de 2opt funcie aan
def two_opt(ExcelInput:str) -> int:
    '''
    We geven hier een string op, wat een excel input word. Is dit geen excel path, gaat de code niet werken
    Het doel van deze functie is om de Running Dinner eerste oplossing te optimaliseren en te schrijven naar 
    de output.xlsx.
    '''


    strafpuntenlijst = list() #Lege lijst voor de plot maken.
    countinteratie = 0 # Alle itteraties die worden berekend kunnen optellen.

    df = pd.read_excel(ExcelInput) # Vanuit de input van de functie de string omschrijven naar een DataFrame. 
    dfcopy = df.copy()  # DataFrame kopiëren om verbeteringen door te kunnen voeren en verslechteringen te negeren.
    improved = True # Om de while loop te kunnen laten lopen is dit van belang. Hierdoor stopt hij nooit met berekenen.

    totale_strafpunten = totaal_som_strafpunten(df) # Beginwaarde van de strafpunten berekenen via functie.

    new_strafpunten = totale_strafpunten    # Kopievariabele maken van strafpunten

    # While loop om te blijven berekenen maar wel de output.xlsx kunnen bijwerken.
    while improved:
        improved = False    # "
        logger.debug(f"Totale aantal strafpunten: {totale_strafpunten}") # Logbestand bijwerken
        
        # Om zo veel mogenlijk opties en iteraties te creëeren randomisen we de 2 huizen waar mensen wonen
        for k in range(3):

            # Dit zijn de verschillende gangen waarover we kunnen optimaliseren.
            gangen = ['Voor', "Hoofd", "Na"]

            # Dit zorgt ervoor dat we een lijst krijgen met alle intergere getallen tussen 0 en lengte van alle mensen
            numbers = list(itertools.chain(range(0, len(df))))

            # Dit zorgt ervoor dat deze getallen worden verwisseld zodat er gerandomised word welke gang met welke wisseld.
            random.shuffle(numbers)

            # Hier pakt hij een gerandomisede getal die hij gaat veranderen.
            # Dit doet hij voor elke getallen. We gebruiken het eerste getal
            for i in (numbers):
                # Hier geven we weer een update in het logbestand
                logger.debug(f"update i: {i}")

                # Hier shuffelen we de nummers weer zodat we het 2e item die we gaan wisselen kunnen randomisen
                random.shuffle(numbers)
                for j in numbers:

                    # Hier tellen we de itteratie som op met 1. Dit gebruiken we voor de plot
                    countinteratie += 1

                    # Hier kiezen we een random gang zodat er een random persoon, en een random gang worden geswitched. 
                    # De gangen randomisen we hier zodat er alleen uit de zelfde gang word verwisseld van mensen.
                    gang_verandering = random.choice(gangen)

                    # Hier kijken we of de gang die we hebben gekozen de gekookte gang is van de persoon die we hebben gekozen.
                    # Als dit zo is, dan slaan we deze iteratie over om aan de constraints te voldoen.
                    if gang_verandering == dfcopy.loc[i,'kookt']:
                        new_strafpunten_copy = totaal_som_strafpunten(dfcopy) 
                        continue

                    # Als dit niet zo is, dan gaan we 2 random mensen met dezelfde gang verwisselen van huis.
                    else:
                        dfcopy.loc[i, gang_verandering], dfcopy.loc[j, gang_verandering] = dfcopy.loc[j, gang_verandering], dfcopy.loc[i, gang_verandering]
                        # Hier berekenen we de strafpunten van de nieuwe dataframe.
                        new_strafpunten_copy = totaal_som_strafpunten(dfcopy)    

                    # Hier kijken we of de verwisseling een verbetering was of niet. 
                    # Is dit het geval dan gaan we door met deze nieuwe dataframe.  
                    # Is dit niet het geval, dan negeren we deze iteratie.       
                    if new_strafpunten_copy < totale_strafpunten:
                        # Hier vervangen we alle variabelen met de verbeterde variabelen zodat 
                        # we een nieuwe iteratie kunnen beginnen
                        new_strafpunten = new_strafpunten_copy
                        totale_strafpunten = new_strafpunten
                        df = dfcopy
                        improved = True

                        # Dit gebruiken we voor debugging
                        print("df heeft geupdate")  
                        strafpuntenlijst.append(totale_strafpunten)
                        # Hier exporteren we de verbeterde DataFrame als output naar een excelbestand
                        df.to_excel("Output.xlsx")  
                        logger.debug(f"Strafpunten has total value: {totale_strafpunten}, i,j={i},{j}")    
        # Hier plotten we de strafpunten tenopzichte van de itteraties         
        plt.plot(countinteratie, strafpuntenlijst)
    # Hier returnen we de strafpunten
    return totale_strafpunten


# Hier geven we het bestand op die we willen 2opt'en
ExcelFile = 'Running Dinner eerste oplossing 2023 v2.xlsx'
two_opt(ExcelFile)



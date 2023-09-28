import pandas as pd
import numpy as np

# 1. Elke deelnemer eet elk gerecht
def controleer_gangen(ExcelInput):
    # Lees het Excel-bestand
    df = pd.read_excel(ExcelInput)

    # Kopieer het dataframe zodat het origineel behouden blijft
    df_new = df.copy()

    def controleer_gang(gang_naam):
        ontbrekende_gang = df[df[gang_naam].isnull()]

        if ontbrekende_gang.empty:
            print(f'iedereen krijgt {gang_naam} gerecht')
        else:
            personen_zonder_gang = ontbrekende_gang['Bewoner'].tolist()
            print(f"Aantal mensen die geen {gang_naam} gerecht krijgen:", len(personen_zonder_gang))
            if len(personen_zonder_gang) > 0:
                print(f"Deze personen hebben geen {gang_naam}gerecht:")
                print(personen_zonder_gang)
                
    def controleer_adressen():
        deelnemers_met_zelfde_adres = []

        for index, row in df.iterrows():
            adressen = [row['Voor'], row['Hoofd'], row['Na']]
            if len(set(adressen)) != len(adressen):
                deelnemers_met_zelfde_adres.append(row['Bewoner'])

        if not deelnemers_met_zelfde_adres:
            print("Elke deelnemer eet elke gang op een ander adres.")
        else:
            print("Deze deelnemers eten dezelfde gangen op hetzelfde adres:")
            print(deelnemers_met_zelfde_adres)
            

    # Roep de functie aan voor verschillende gangen
    controleer_gang('Voor')
    controleer_gang('Hoofd')
    controleer_gang('Na')
    
    # Controleer adressen
    controleer_adressen()

# Roep de functie aan met het pad naar je Excel-bestand als argument
#controleer_gangen('Running Dinner eerste oplossing 2022.xlsx')


# 2. iedereen eet elk gerecht op een ander adres. Een persoon zit dus niet 2 gangen op hetzelfde adres



# 3. elk huishouden dat niet is vrijgesteld van koken, maakt 1 van de 3 gangen.

  
# 4. zorgen dat er niet wordt gegeten op een adres waar niet wordt gekookt

def huisadressen_niet_koken(ExcelInput):
    df = pd.read_excel(ExcelInput)
    niet_koken = set()

    #Identificeer de deelnemers die niet hoeven te koken
    for index, row in df.iterrows():
        if pd.isna(row['kookt']):
            niet_koken.add(row['Huisadres'])    

    return niet_koken

def deelnemers_op_huisadres(ExcelInput, adres):
    df = pd.read_excel(ExcelInput)

    #Controleer of het adres voorkomt in de kolommen 'Voor', 'Hoofd' en 'Na' voor andere deelnemers
    deelnemers = df[(df['Voor'] == adres) | (df['Hoofd'] == adres) | (df['Na'] == adres)]['Bewoner'].tolist()

    return deelnemers

#Roep de functies aan
niet_koken_adressen = huisadressen_niet_koken('Running Dinner eerste oplossing 2022.xlsx')

for adres in niet_koken_adressen:
    deelnemers = deelnemers_op_huisadres('Running Dinner eerste oplossing 2022.xlsx', adres)
    if deelnemers:
        print(f"Deelnemers die op {adres} eten terwijl er niet wordt gekookt: {', '.join(deelnemers)}")











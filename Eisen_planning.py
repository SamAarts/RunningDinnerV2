import pandas as pd
import numpy as np
ExcelFile = 'Running Dinner eerste oplossing 2022.xlsx'

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
controleer_gangen(ExcelFile)


# 2. elk huishouden dat niet is vrijgesteld van koken, maakt 1 van de 3 gangen.
def iedereen_een_gang(ExcelInput):
    df = pd.read_excel(ExcelInput)
    gezien_adressen = {}  # Een dictionary om bij te houden welke adressen al gezien zijn

    for index, row in df.iterrows():
        if not pd.isnull(row['kookt']):
            if row['Huisadres'] in gezien_adressen:
                # Dit adres is al gezien, controleer of de kookwaarde hetzelfde is
                if row['kookt'] != gezien_adressen[row['Huisadres']]:
                    print(f"Dit adres {row['Huisadres']} heeft een conflict: {gezien_adressen[row['Huisadres']]} en nu {row['kookt']}")
            else:
                gezien_adressen[row['Huisadres']] = row['kookt']  # Voeg het adres toe aan de lijst van gezien adressen
            
            # Controleer of het huisadres overeenkomt met de kolomnaam van de kookwaarde
            if row['Huisadres'] != row[row['kookt']]:
                print(f"Het huisadres {row['Huisadres']} komt niet overeen met het adres onder de kolom '{row['kookt']}'.")


iedereen_een_gang(ExcelFile)

  
# 3. zorgen dat er niet wordt gegeten op een adres waar niet wordt gekookt.
# Wanneer een deelnemer een bepaalde gang moet koken is deze deelnemer voor die gang ingedeeld op diens eigen adres.

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
niet_koken_adressen = huisadressen_niet_koken(ExcelFile)

for adres in niet_koken_adressen:
    deelnemers = deelnemers_op_huisadres(ExcelFile, adres)
    if deelnemers:
        print(f"Deelnemers die op {adres} eten terwijl er niet wordt gekookt: {', '.join(deelnemers)}")


# 4. Het aantal tafelgenoten dat op een bepaald huisadres eet, voldoet aan de bij het adres horende minimum en maximum groepsgrootte.
# def aantal_tafelgenoten(ExcelInput):
#     df = pd.read_excel(ExcelInput)
    
# aantal_tafelgenoten(ExcelFile)



# def controle_huisadressen(ExcelInput):
#     df = pd.read_excel(ExcelInput)
    
#     # Maak een dictionary om het maximum aantal deelnemers per huisadres bij te houden
#     # max_aantal_dict = {}
#     # for index, row in df.iterrows():
#     #     if row['Huisadres'] not in max_aantal_dict:
#     #         max_aantal_dict[row['Huisadres']] = row['aantal']
    
#     huisadres_teller = {}
    
#     # Loop door de rijen en verhoog de teller als het adres opnieuw voorkomt in elke kolom
#     for index, row in df.iterrows():
#         kolommen = ['Voor', 'Hoofd', 'Na']
#         for kolom in kolommen:
#             if row[kolom] in huisadres_teller:
#                 huisadres_teller[row[kolom]] += 1
#             else:
#                 huisadres_teller[row[kolom]] = 1
    
#     return huisadres_teller

# # Roep de functie aan met het Excel-bestand 'ExcelFile'
# resultaat = controle_huisadressen(ExcelFile)

# print("Aantal voorkomens per huisadres:")
# print(resultaat)
    
    # # Controleer of het aantal deelnemers het maximum overschrijdt
    # overtredingen = {}
    # for adres, telling in huisadres_teller.items():
    #     if telling > max_aantal_dict[adres]:
    #         overtredingen[adres] = telling
    
    # return overtredingen

# Roep de functie aan met het Excel-bestand 'ExcelFile'
# overtredingen = controle_huisadressen(ExcelFile)

# print("Huisadressen met overschrijdingen:")
# print(overtredingen)



# def aantal_huisadressen_per_kolom(ExcelInput):
#     df = pd.read_excel(ExcelInput)
    
#     # Maak een lege dictionary voor elke kolom
#     voor_teller = {}
#     hoofd_teller = {}
#     na_teller = {}
#     max_aantal_dict = {}
    
#     # Vul de maximaal toegestane aantallen in de juiste dictionary
#     for index, row in df.iterrows():
#         if row['aantal'] in max_aantal_dict:
#             max_aantal_dict[row['Huisadres']] = row['aantal']
    
#     # Loop door de rijen en verhoog de teller voor elk huisadres in de betreffende kolom
#     for index, row in df.iterrows():
#         if row['Voor'] in voor_teller:
#             voor_teller[row['Voor']] += 1
#         else:
#             voor_teller[row['Voor']] = 1
        
#         if row['Hoofd'] in hoofd_teller:
#             hoofd_teller[row['Hoofd']] += 1
#         else:
#             hoofd_teller[row['Hoofd']] = 1
        
#         if row['Na'] in na_teller:
#             na_teller[row['Na']] += 1
#         else:
#             na_teller[row['Na']] = 1
    
#     return {'Voor': {'Huisadres': list(voor_teller.keys()), 'voor_teller': list(voor_teller.values()), 'max_aantal_dict': max_aantal_dict},
#             'Hoofd': {'Huisadres': list(hoofd_teller.keys()), 'hoofd_teller': list(hoofd_teller.values()), 'max_aantal_dict': max_aantal_dict},
#             'Na': {'Huisadres': list(na_teller.keys()), 'na_teller': list(na_teller.values()), 'max_aantal_dict': max_aantal_dict}}

# # Roep de functie
# resultaten = aantal_huisadressen_per_kolom(ExcelFile)

# # Print de resultaten voor 'Voor'
# print("Voor:")
# print("Huisadres | Voor Teller | Maximaal Aantal")
# for i in range(len(resultaten['Voor']['Huisadres'])):
#     print(f"{resultaten['Voor']['Huisadres'][i]} | {resultaten['Voor']['voor_teller'][i]} | {resultaten['Voor']['max_aantal_dict'][resultaten['Voor']['Huisadres'][i]]}")

# # Print de resultaten voor 'Hoofd'
# print("\nHoofd:")
# print("Huisadres | Hoofd Teller | Maximaal Aantal")
# for i in range(len(resultaten['Hoofd']['Huisadres'])):
#     print(f"{resultaten['Hoofd']['Huisadres'][i]} | {resultaten['Hoofd']['hoofd_teller'][i]} | {resultaten['Hoofd']['max_aantal_dict'][resultaten['Hoofd']['Huisadres'][i]]}")

# # Print de resultaten voor 'Na'
# print("\nNa:")
# print("Huisadres | Na Teller | Maximaal Aantal")
# for i in range(len(resultaten['Na']['Huisadres'])):
#     print(f"{resultaten['Na']['Huisadres'][i]} | {resultaten['Na']['na_teller'][i]} | {resultaten['Na']['max_aantal_dict'][resultaten['Na']['Huisadres'][i]]}")



# import pandas as pd

# def tel_huisadressen_voor(ExcelInput):
#     df = pd.read_excel(ExcelInput)
    
#     # Maak een lege dictionary om de resultaten op te slaan
#     resultaten = {}
    
#     # Loop door de rijen en vul de resultaten dictionary
#     for index, row in df.iterrows():
#         huisadres = row['Huisadres']
#         voorgerechten = row['Voor']
#         aantal_toegestane_gasten = row['aantal']
        
#         if pd.isnull(aantal_toegestane_gasten):
#             continue
#         else:
#             if voorgerechten in resultaten:
#                 resultaten[huisadres][voorgerechten]['aantal_voor'] += 1
#             else:
#                 resultaten[huisadres][voorgerechten]['aantal_voor'] == 1

    
#     return resultaten

# # Roep de functie aan met het Excel-bestand ExcelFile
# resultaat_voor = tel_huisadressen_voor(ExcelFile)

# # Print de resultaten
# for huisadres, info in resultaat_voor.items():
#     print(f"Huisadres: {huisadres}, Aantal in 'Voor': {info['aantal_voor']}, Aantal toegestane gasten: {info['aantal_toegestane_gasten']}")

import pandas as pd

def tel_huisadressen_voor(ExcelInput):
    df = pd.read_excel(ExcelInput)
    
    # Maak een lege dictionary om de resultaten op te slaan
    resultaten = {}
    
    # Loop door de rijen en vul de resultaten dictionary
    for _, row in df.iterrows():
        huisadres = row['Huisadres']
        voorgerechten = row['Voor']
        aantal_toegestane_gasten = row['aantal']
        
        if pd.notna(aantal_toegestane_gasten):
            if huisadres in resultaten:
                if voorgerechten in resultaten[huisadres]:
                    resultaten[huisadres][voorgerechten]['aantal_voor'] += 1
                else:
                    resultaten[huisadres][voorgerechten] = {'aantal_voor': 1, 'aantal_toegestane_gasten': aantal_toegestane_gasten}
            else:
                resultaten[huisadres] = {voorgerechten: {'aantal_voor': 1, 'aantal_toegestane_gasten': aantal_toegestane_gasten}}
        else:
            continue
            
    return resultaten

# Roep de functie aan met het Excel-bestand ExcelFile
resultaat_voor = tel_huisadressen_voor(ExcelFile)

# Print de resultaten
for huisadres, info in resultaat_voor.items():
    print(f"Huisadres: {huisadres}, Aantal in 'Voor': {info['aantal_voor']}, Aantal toegestane gasten: {info['aantal_toegestane_gasten']}")

import pandas as pd
import numpy as np
pd.options.mode.chained_assignment = None
ExcelFile = 'Running Dinner eerste oplossing 2022.xlsx'
ExcelData = 'Running Dinner dataset 2022.xlsx'

# 1. Elke deelnemer eet elk gerecht
def controleer_gangen(ExcelInput):
    """
    Controleert de gangen in de opgegeven Excel-file en geeft informatie over ontbrekende gerechten
    en deelnemers die op hetzelfde adres zitten.

    Args:
        ExcelInput (str): De bestandsnaam (en pad) van het Excel-bestand met de tafelindeling.

    Returns:
        None
    """
    # Lees het Excel-bestand
    df = pd.read_excel(ExcelInput)

    def controleer_gang(gang_naam):
        """
        Controleert de opgegeven gang en geeft informatie over ontbrekende gerechten.

        Args:
            gang_naam (str): De naam van de gang ('Voor', 'Hoofd' of 'Na').

        Returns:
            None
        """
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
        """
        Controleert of er deelnemers zijn met hetzelfde adres en geeft deze deelnemers weer.

        Returns:
            None
        """
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
    """
    Controleert of elke persoon die kookt een gang heeft toegewezen gekregen.

    Args:
        ExcelInput (str): De bestandsnaam (en pad) van het Excel-bestand.

    Returns:
        None
    """
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
    """
    Identificeert de huisadressen waar geen kookinformatie beschikbaar is.

    Args:
        ExcelInput (str): De bestandsnaam (en pad) van het Excel-bestand.

    Returns:
        set: Een set met de huisadressen waar geen kookinformatie beschikbaar is.
    """
    df = pd.read_excel(ExcelInput)
    niet_koken = set()

    #Identificeer de deelnemers die niet hoeven te koken
    for index, row in df.iterrows():
        if pd.isna(row['kookt']):
            niet_koken.add(row['Huisadres'])    

    return niet_koken

def deelnemers_op_huisadres(ExcelInput, adres):
    """
    Geeft een lijst van deelnemers die op het opgegeven huisadres eten.

    Args:
        ExcelInput (str): De bestandsnaam (en pad) van het Excel-bestand.
        adres (str): Het huisadres waarop wordt gezocht.

    Returns:
        list: Een lijst van deelnemers die op het opgegeven huisadres eten.
    """
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
# is dit wel nodig, want we krijgen een toegelaten oplossing. Want als je mensen gaat wisselen dan blijven het er even veel

# 5. Enkele duo's zitten elke gang bij elkaar aan tafel

def paren_bij_elkaar(ExcelInput, DataSet):
    """
    Zoekt naar bewoners die bij elkaar moeten blijven tijdens het eten op basis van de gegeven datasets.

    Args:
        ExcelInput (str): De bestandsnaam (en pad) van het Excel-bestand met de tafelindeling.
        DataSet (str): De bestandsnaam (en pad) van het Excel-bestand met de gegevens over welke paren bij elkaar moeten blijven.

    Returns:
        None
    """
    df = pd.read_excel(ExcelInput)
    df2 = pd.read_excel(DataSet, sheet_name='Paar blijft bij elkaar', skiprows=[0]) 

    gevonden_bewoners = []
    gevonden_df = pd.DataFrame(columns=df.columns)
    Moeten_bij_elkaar_blijven = list()
    
    for i in df['Bewoner']:
        for j in df2['Bewoner1']:
            if i == j:
                index = df2[df2['Bewoner1'] == j].index[0]
                Moeten_bij_elkaar_blijven.append(i)
                Moeten_bij_elkaar_blijven.append(df2["Bewoner2"].iloc[index])
                #print(f'Bewoner {i} moet bij elke gang bij bewoner {df2["Bewoner2"].iloc[index]} zitten.')

                gevonden_bewoners.append(i)
                
                # Haal de gehele rij van df op voor de eerste bewoner
                gevonden_rij_df = df.loc[df['Bewoner'] == i]
                gevonden_rij_df = gevonden_rij_df.drop(gevonden_rij_df.columns[0], axis=1)

                # Voeg de rij toe aan het gevonden dataframe
                gevonden_df = pd.concat([gevonden_df, gevonden_rij_df])
    

    # Voeg de informatie toe van de gekoppelde bewoners
    for bewoner in gevonden_bewoners:
        gekoppelde_bewoner_df = df2.loc[df2['Bewoner1'] == bewoner]
        for gekoppelde_bewoner in gekoppelde_bewoner_df['Bewoner2']:
            gevonden_rij_df = df.loc[df['Bewoner'] == gekoppelde_bewoner]
            gevonden_rij_df = gevonden_rij_df.drop(gevonden_rij_df.columns[0], axis=1)
            gevonden_df = pd.concat([gevonden_df, gevonden_rij_df])

    gevonden_df = gevonden_df.drop(gevonden_df.columns[0], axis=1)
    gevonden_df = gevonden_df.sort_values(by=['Bewoner'])
    gevonden_df = gevonden_df.reset_index(drop=True)

    Groterelijst = list()

    for i in range(0, len(gevonden_df), 2):
        koppelheeftnodigomteslagen = list()
        for j in range(2,5):
            koppelheeftnodigomteslagen.append(gevonden_df.iloc[i,j])
        
        Groterelijst.append(koppelheeftnodigomteslagen)


    gangen = ['Voor', 'Hoofd', "Na"]
    MensenNaElkaarBijElkaarGangNaGang = list()
    for i in gangen:
        for j in range(len(gevonden_df)):
            if gevonden_df[i][j] == gevonden_df[i][j]:
                MensenNaElkaarBijElkaarGangNaGang.append(gevonden_df[i][j])
    
    has_isolated_data_point = False


    for i in range(1, len(MensenNaElkaarBijElkaarGangNaGang) - 1):
        if MensenNaElkaarBijElkaarGangNaGang[i] != MensenNaElkaarBijElkaarGangNaGang[i - 1] and MensenNaElkaarBijElkaarGangNaGang[i] != MensenNaElkaarBijElkaarGangNaGang[i + 1]:
            has_isolated_data_point = True
            break   
    
    if has_isolated_data_point == True:
        print("Paren die bij elkaar moeten blijven doen dit niet")
    else:
        print("Paren die bij elkaar moeten blijven doen dit")
    # print(Groterelijst)
    # for i in Groterelijst:
    #     for j in i:
    #         for l in range(2,5):
    #             gevonden_df[]
    #         print(j)
        
        

paren_bij_elkaar(ExcelFile, ExcelData)



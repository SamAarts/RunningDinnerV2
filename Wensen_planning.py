
import pandas as pd
import numpy as np 
from collections import defaultdict


#Onnodige foutcode verhelpen
pd.options.mode.chained_assignment = None

def Voorkeursgang(df):
    """
    Controleert of de voorkeursgang van de deelnemers overeenkomt met de oplossing.

    De functie leest de Excel-bestanden, verwijdert onnodige kolommen en reset de indices. Vervolgens wordt gecontroleerd of 
    de voorkeursgangen in de dataset overeenkomen met de oplossing. Strafpunten worden toegekend voor elke onjuiste voorkeursgang.

    Returns:
        int: Het totaal aantal strafpunten voor onjuiste voorkeursgangen.
    """

    # Excel inladen en juiste dataframe van maken.
    dfdataset= pd.read_excel('Running Dinner dataset 2023 v2.xlsx', sheet_name='Adressen').drop(['Min groepsgrootte', 'Max groepsgrootte'], axis=1).reset_index(drop=True)
    dfoplossing = df
    # Lege lijsten en tellingen aanmaken.
    huizenmetvoorkeur = list()
    countVoorkeursgang = 0
    gangmetvoorkeur = list()

    # Kijken of er een voorkeur is, het huis en de bijbehorende gang in een lijst zetten.
    for i in range(len(dfdataset)):
        if type(dfdataset.iloc[i]["Voorkeur gang"]) == str:
            huizenmetvoorkeur.append(dfdataset.iloc[i]['Huisadres'])
            gangmetvoorkeur.append(dfdataset.iloc[i]['Voorkeur gang'])
            

    # Kijken of een huis uit de dataframe van de 2opt een voorkeur heeft.
    # Kijken of dat huis hetzelfde gerecht kookt als zijn voorkeur.
    # Strafpunten toe eisen als dit niet het geval is.
    for i in range(len(dfoplossing)):
        for j in range(len(huizenmetvoorkeur)):
            if dfoplossing.iloc[i]['Huisadres'] == huizenmetvoorkeur[j]:
                if dfoplossing.iloc[i]['kookt'] != gangmetvoorkeur[j]:
                    print(f"dit huis kookt niet zijn voorkeur {dfoplossing.iloc[i]['Huisadres']}")
                    countVoorkeursgang += 4
    # Strafpunten terug geven voor de totale punten telling.
    return  countVoorkeursgang


def Tafelburen2022(df):
    """
    Controleert of er deelnemers zijn die in zowel 2022 als 2023 naast elkaar aan tafel zitten en kent strafpunten toe.
    Dit gebeurd alleen als dit nodig is. Hiervoor word hetvolgde gedaan.

    De functie laadt de oplossingen voor 2022 en 2023, en vervolgens worden de huizen per inwoner bepaald. Als een deelnemer
    in zowel 2022 als 2023 naast dezelfde persoon aan tafel zit, worden strafpunten toegekend.

    Returns:
        int: Het totaal aantal strafpunten voor deelnemers die in zowel 2022 als 2023 naast elkaar aan tafel zitten.
    """
    # Tellingen aanmaken en dataframes aanmaken.
    countTafelburen2022 = 0
    dfOplossing2023 = df
    dfOplossing2022 = pd.read_excel('Running Dinner eerste oplossing 2022.xlsx')

    # DataFrame opschonen.
    dfOplossing2022['Voor'] = dfOplossing2022['Voor'].str.replace(r'(\d+)', r'_\1', regex=True)
    dfOplossing2022['Hoofd'] = dfOplossing2022['Hoofd'].str.replace(r'(\d+)', r'_\1', regex=True)
    dfOplossing2022['Na'] = dfOplossing2022['Na'].str.replace(r'(\d+)', r'_\1', regex=True)

    # Lege dict om te kijken welk persoon bij welk huis zit. Dit voor 2023.
    HuizenPerInwoner2023 = dict()
    for i in range(len(dfOplossing2023)):   
        tijdelijk2023 = dfOplossing2023.loc[i].tolist()
        HuizenPerInwoner2023[tijdelijk2023[1]] = tijdelijk2023[3:6]

    # Lege dict om te kijken welk persoon bij welk huis zit. Dit voor 2022.
    HuizenPerInwoner2022 = dict()
    for i in range(len(dfOplossing2022)):   
        tijdelijk2022 = dfOplossing2022.loc[i].tolist()
        HuizenPerInwoner2022[tijdelijk2022[1]] = tijdelijk2022[3:6]

    # Lijst aan maken voor alle mensen die vorig jaar al bij elkaar aan tafel zaten.
    DubbeleMensenVan2022en2023 = list()
    for i in HuizenPerInwoner2023:
        for j in HuizenPerInwoner2022:
            for k in range(0,2):
                for l in range(0,2):
                    # Voor iedereen word gecontroleerd met wie ze vorig jaar en dit jaar aantafel zitten. 
                    # Zitten ze met dezelfde mensen aantafel worden er strafpunten van 3 toegewezen.
                    if HuizenPerInwoner2023[i][k] == HuizenPerInwoner2022[j][l]:
                        if HuizenPerInwoner2023[i][k] not in DubbeleMensenVan2022en2023:
                            DubbeleMensenVan2022en2023.append(HuizenPerInwoner2023[i][k])
                            countTafelburen2022 += 3
    # Hier word een integer getal teruggegeven aan de hand van de hoeveelheid strafpunten.
    return countTafelburen2022 
                      
    


def Tafelburen2021(df):
    """
    Controleert of er deelnemers zijn die in zowel 2021 als 2023 naast elkaar aan tafel zitten en kent strafpunten toe.
    Dit gebeurd alleen als dit nodig is. Hiervoor word hetvolgde gedaan.
    
    De functie laadt de oplossingen voor 2021 en 2023, en voert vervolgens enkele bewerkingen uit op de kolommen.
    Vervolgens worden de huizen per inwoner bepaald. Als een deelnemer in zowel 2021 als 2023 naast dezelfde persoon aan tafel
    zit, worden strafpunten toegekend.

    Returns:
        int: Het totaal aantal strafpunten voor deelnemers die in zowel 2021 als 2023 naast elkaar aan tafel zitten.
    """
    # Tellingen aanmaken en dataframes inladen.
    countTafelburen2021 = 0
    dfOplossing2023 = df
    dfOplossing2021 = pd.read_excel('Running Dinner eerste oplossing 2021 - corr.xlsx')

    # Data om DataFrame op te kunnen schonen
    columns_to_add_underscore = ['Voor', 'Hoofd', 'Na']

    # Hier word een _ toegevoegd bij elk huis tussen het getal en de letters om de 
    # juiste structuur aan te kunnen blijven houden in het DataFrame.
    for column in columns_to_add_underscore:
        dfOplossing2021[column] = dfOplossing2021[column].apply(lambda x: x[0] + '_' + x[1:] if len(x) > 1 and x[0].isalpha() else x)
    

    # Hier word de juiste extra letter toegevoegd aan elk huishouden om het generiek te houden
    for column in columns_to_add_underscore:
        for i in range(len(dfOplossing2023)):
            if dfOplossing2023[column][i][0] == 'W':
                dfOplossing2023[column][i] = dfOplossing2023[column][i][0] + 'O' +dfOplossing2023[column][i][2:]
            elif dfOplossing2023[column][i][0] == "V":
                dfOplossing2023[column][i] = dfOplossing2023[column][i][0] + 'W' +dfOplossing2023[column][i][2:]

    # Lege dict om te kijken welk persoon bij welk huis zit. Dit voor 2023.
    HuizenPerInwoner2023 = dict()
    for i in range(len(dfOplossing2023)):   
        tijdelijk2023 = dfOplossing2023.loc[i].tolist()
        HuizenPerInwoner2023[tijdelijk2023[1]] = tijdelijk2023[3:6]

    # Lege dict om te kijken welk persoon bij welk huis zit. Dit voor 2021.
    HuizenPerInwoner2021 = dict()
    for i in range(len(dfOplossing2021)):   
        tijdelijk2021 = dfOplossing2021.loc[i].tolist()
        HuizenPerInwoner2021[tijdelijk2021[1]] = tijdelijk2021[3:6]

    # Lijst aan maken voor alle mensen die vorig jaar al bij elkaar aan tafel zaten.   
    DubbeleMensenVan2021en2023 = list()
    for i in HuizenPerInwoner2023:
        for j in HuizenPerInwoner2021:
            for k in range(0,2):
                for l in range(0,2):
                    if HuizenPerInwoner2023[i][k] == HuizenPerInwoner2021[j][l]:
                    # Voor iedereen word gecontroleerd met wie ze vorig jaar en dit jaar aantafel zitten. 
                    # Zitten ze met dezelfde mensen aantafel worden er strafpunten van 3 toegewezen.
                        if HuizenPerInwoner2023[i][k] not in DubbeleMensenVan2021en2023:
                            DubbeleMensenVan2021en2023.append(HuizenPerInwoner2023[i][k])
                            countTafelburen2021 += 1
    return countTafelburen2021



def TafelburenGeenEchteBuren(df):
    """
    Controleert de burenrelaties van deelnemers en bepaalt of ze naast elkaar aan tafel zitten.

    De functie laadt de oplossing voor 2023, de dataset met bureninformatie en de dataset met bewonersinformatie. Vervolgens
    wordt een mapping gemaakt van bewoners naar hun huisadressen en toegepast op de bureninformatie. Het resultaat wordt
    in een nieuw DataFrame samengevoegd en geprint.

    Returns:
        None
    """
    try:  
        dfOplossing = df
        df = pd.read_excel('Running Dinner dataset 2023 v2.xlsx').drop(columns=['Kookt niet']).sort_values(by=['Bewoner'])
        dftijdelijk = pd.read_excel("Running Dinner dataset 2023 v2.xlsx", sheet_name='Buren').drop([0])
        dftijdelijk.rename(columns={'De volgende bewoners zijn directe buren': 'Bewoner', "Unnamed: 1":"Buren"}, inplace=True)
        dftijdelijk = dftijdelijk.sort_values(by=['Bewoner'])
        df = df.merge(dftijdelijk, on= "Bewoner")
        df = df.sort_values(by='Buren')
        bewoner_to_huisadres = df.set_index('Bewoner')['Huisadres'].to_dict()
        df['BurenAdres'] = df['Buren'].map(bewoner_to_huisadres)

        dfOplossing = dfOplossing.drop(columns=['Unnamed: 0', "kookt", 'aantal'])    
        BuurmanCount = 0
        for i in range(len(dfOplossing['Bewoner'])):
            for j in range(len(df["Bewoner"])):
                if df.iloc[j,2] == dfOplossing.iloc[i, 0]:
                    for l in range(2,5):
                        if dfOplossing.iloc[i,l] == df.iloc[j,1]:
                            BuurmanCount += 1
        return BuurmanCount
    
    except Exception as e:
        BuurmanCount = 0
        for i in range(len(dfOplossing['Bewoner'])):
            for j in range(len(df["Bewoner"])):
                if df.iloc[j,2] == dfOplossing.iloc[i, 0]:
                    for l in range(2,5):
                        if dfOplossing.iloc[i,l] == df.iloc[j,1]:
                            BuurmanCount += 1

        BuurmanCount = int(BuurmanCount/2)
        return BuurmanCount


def HoofdgerechtVorigJaar(df):
    """
    Controleert of deelnemers die vorig jaar het hoofdgerecht kookten, dit jaar opnieuw het hoofdgerecht koken.

    Deze functie vergelijkt de oplossingen voor 2022 en 2023 om te bepalen welke deelnemers vorig jaar het hoofdgerecht
    kookten en dit jaar opnieuw het hoofdgerecht koken. Strafpunten worden toegekend voor deelnemers die vorig jaar het
    hoofdgerecht kookten, maar dit jaar niet.

    Args:
        df (pandas.DataFrame): Het DataFrame met de gegevens van deelnemers voor 2023.

    Returns:
        int: Het totale aantal strafpunten voor deelnemers die vorig jaar het hoofdgerecht kookten, maar dit jaar niet.
    """
    dfOplossing2023 = df
    dfOplossing2022 = pd.read_excel('Running Dinner eerste oplossing 2022.xlsx')

    dfnieuw = dfOplossing2022.drop(['Unnamed: 0','Huisadres','Voor','Hoofd','Na', 'aantal'], axis=1)
    hoofdgerechtchefs2022 = list()
    for i in range(len(dfnieuw)):
        if dfnieuw['kookt'][i] == "Hoofd":
            hoofdgerechtchefs2022.append(dfnieuw['Bewoner'][i])

    dfnieuw2 = dfOplossing2023.drop(['Unnamed: 0','Huisadres','Voor','Hoofd','Na', 'aantal'], axis=1)
    hoofdgerechtchefs2023 = list()
    for i in range(len(dfnieuw2)):
        if dfnieuw2['kookt'][i] == "Hoofd":
            hoofdgerechtchefs2023.append(dfnieuw2['Bewoner'][i])    
    countHoofdgerechtVorigJaar = 0
    for chef2022 in hoofdgerechtchefs2022:
        if chef2022 in hoofdgerechtchefs2023:
            countHoofdgerechtVorigJaar += 5

    return countHoofdgerechtVorigJaar


def niet_bij_elkaar(df):
    """
    Deze functie berekent het aantal keren dat bewoners elkaar tegenkomen tijdens verschillende gangen,
    waarbij ze zo min mogelijk bij elkaar aan tafel mogen zitten. Het resultaat is het aantal keren dat dit voorkomt,
    vermenigvuldigd met 6 (dit omdat het een strenge eis is).

    Args:
        ExcelInput (str): De bestandsnaam (en pad) van het Excel-bestand met de tafelindeling.

    Returns:
        int: Het totale aantal keren dat bewoners elkaar tegenkomen en niet bij elkaar mogen zitten, vermenigvuldigd met 6.
    """
    count_niet_bij_elkaar = 0
    # Lees het Excel-bestand
    #df = pd.read_excel(ExcelInput)
    
def niet_bij_elkaar(df):
    """
    Bereken strafpunten op basis van de frequentie van individuen die dezelfde locaties delen.

    Deze functie berekent strafpunten op basis van het aantal keren dat individuen worden
    waargenomen op dezelfde 'Voor', 'Hoofd' of 'Na' locaties. Een strafpunt wordt toegekend
    wanneer twee verschillende individuen worden waargenomen op dezelfde locaties.

    Args:
        df (DataFrame): Een DataFrame met gegevens met kolommen 'Bewoner', 'Voor', 'Hoofd' en 'Na'.

    Returns:
        int: Het totale aantal strafpunten voor individuen die samen worden waargenomen op dezelfde locaties.
    """
    
    GrotePersonenDict = defaultdict(int)
    
    # Maak benodigde series van elke rij in het DataFrame
    for i in range(len(df)):
        Mens1 = df.at[i, 'Bewoner']
        locatie_voor = df.at[i, 'Voor']
        locatie_hoofd = df.at[i, 'Hoofd']
        locatie_na = df.at[i, 'Na']
        
        # Stap 2: Loop door de rest van de rijen om vergelijkingen te maken
        for j in range(i + 1, len(df)):
            Mens2 = df.at[j, 'Bewoner']
            
            # Stap 3: Controleer of Mens1 en Mens2 verschillende individuen zijn
            if Mens1 != Mens2:
                
                # Stap 4: Controleer of ze dezelfde 'Voor' locatie delen
                if df.at[j, 'Voor'] == locatie_voor:
                    GrotePersonenDict[(Mens1, Mens2)] += 1
                
                # Stap 5: Controleer of ze dezelfde 'Hoofd' locatie delen
                if df.at[j, 'Hoofd'] == locatie_hoofd:
                    GrotePersonenDict[(Mens1, Mens2)] += 1
                
                # Stap 6: Controleer of ze dezelfde 'Na' locatie delen
                if df.at[j, 'Na'] == locatie_na:
                    GrotePersonenDict[(Mens1, Mens2)] += 1

    # Stap 7: Tel het aantal imperfecties met meer dan 1 waarneming
    aantal_imperfecties = sum(1 for value in GrotePersonenDict.values() if value > 1)
    
    # Stap 8: Bereken strafpunten op basis van imperfecties
    Strafpunten_mensen_vaker_elkaar_zien = aantal_imperfecties * 6
    
    return int(Strafpunten_mensen_vaker_elkaar_zien)

    
def totaal_som_strafpunten(df):
    """
    Berekent de totale som van strafpunten door verschillende functies op te roepen en hun resultaten op te tellen.

    Returns:
        int: De totale som van strafpunten.
    """

    # Hier runt hij alle andere code om een overal een int waarde aan te kunnen hangen
    strafpunten_hoofdgerecht_vorig_jaar = HoofdgerechtVorigJaar(df)
    strafpunten_tafelburen_2021 = Tafelburen2021(df)
    strafpunten_tafelburen_2022 = Tafelburen2022(df)
    strafpunten_voorkeursgang = Voorkeursgang(df)
    strafpunten_niet_bij_elkaar= niet_bij_elkaar(df)
    strafpunten_buren_bij_buren = TafelburenGeenEchteBuren(df)
    
    # Dit is de som van alle constraints
    totale_strafpunten = (
        strafpunten_hoofdgerecht_vorig_jaar +
        strafpunten_tafelburen_2021 +
        strafpunten_tafelburen_2022 +
        strafpunten_voorkeursgang +
        strafpunten_niet_bij_elkaar +
        strafpunten_buren_bij_buren
    )
    # Dit is de output van het totaal aantal strafpunten
    return int(totale_strafpunten)

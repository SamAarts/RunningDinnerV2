
import pandas as pd
import numpy as np 

#Onnodige foutcode verhelpen
pd.options.mode.chained_assignment = None

def Voorkeursgang():
    """
    Controleert of de voorkeursgang van de deelnemers overeenkomt met de oplossing.

    De functie leest de Excel-bestanden, verwijdert onnodige kolommen en reset de indices. Vervolgens wordt gecontroleerd of 
    de voorkeursgangen in de dataset overeenkomen met de oplossing. Strafpunten worden toegekend voor elke onjuiste voorkeursgang.

    Returns:
        int: Het totaal aantal strafpunten voor onjuiste voorkeursgangen.
    """

    # Load the Excel files, drop unnecessary columns, and reset the indices
    dfdataset= pd.read_excel('Running Dinner dataset 2023 v2.xlsx', sheet_name='Adressen').drop(['Min groepsgrootte', 'Max groepsgrootte'], axis=1).reset_index(drop=True)
    dfoplossing = pd.read_excel('Running Dinner eerste oplossing 2023 v2.xlsx')
    huizenmetvoorkeur = list()
    voorkeurslijstdataset = list()
    voorkeursgerecht = list()
    countVoorkeursgang = 0
    for i in range(len(dfdataset)):
        if type(dfdataset.iloc[i]["Voorkeur gang"]) == str:
            huizenmetvoorkeur.append(dfdataset.iloc[i]['Huisadres'])
            voorkeurslijstdataset.append(dfdataset.iloc[i]['Huisadres'] + ' ' + dfdataset.iloc[i]['Voorkeur gang'])
            

    voorkeurslijstoplossing = list()
    for i in range(len(dfoplossing)):
        if dfoplossing.iloc[i]['Huisadres'] in huizenmetvoorkeur:
            voorkeurslijstoplossing.append(dfoplossing.iloc[i]['Huisadres'] +' ' + dfoplossing.iloc[i]['kookt'])
            


    for i in range(len(voorkeurslijstoplossing)):
        if voorkeurslijstoplossing[i] not in voorkeurslijstdataset:
            print(f'jij klopt niet {voorkeurslijstoplossing[i]}')
            countVoorkeursgang += 4

    return  countVoorkeursgang
        

## hij print welk gerecht hij wel doet
# Voorkeursgang()

def Tafelburen2022():
    """
    Controleert of er deelnemers zijn die in zowel 2022 als 2023 naast elkaar aan tafel zitten en kent strafpunten toe.

    De functie laadt de oplossingen voor 2022 en 2023, en vervolgens worden de huizen per inwoner bepaald. Als een deelnemer
    in zowel 2022 als 2023 naast dezelfde persoon aan tafel zit, worden strafpunten toegekend.

    Returns:
        int: Het totaal aantal strafpunten voor deelnemers die in zowel 2022 als 2023 naast elkaar aan tafel zitten.
    """
    countTafelburen2022 = 0
    dfOplossing2023 = pd.read_excel('Running Dinner eerste oplossing 2023 v2.xlsx')
    dfOplossing2022 = pd.read_excel('Running Dinner eerste oplossing 2022.xlsx')

    dfOplossing2022['Voor'] = dfOplossing2022['Voor'].str.replace(r'(\d+)', r'_\1', regex=True)
    dfOplossing2022['Hoofd'] = dfOplossing2022['Hoofd'].str.replace(r'(\d+)', r'_\1', regex=True)
    dfOplossing2022['Na'] = dfOplossing2022['Na'].str.replace(r'(\d+)', r'_\1', regex=True)
    ## kijken welke mensen in welk huis zaten per gang. lijst met unique huizen maken en mensen aan huizen toevoegen.
    ## Dit voor 2022 en 2023 doen. Als er 1 overeen komt, 1 strafpunt erbij
    HuizenPerInwoner2023 = dict()
    for i in range(len(dfOplossing2023)):   
        tijdelijk2023 = dfOplossing2023.loc[i].tolist()
        HuizenPerInwoner2023[tijdelijk2023[1]] = tijdelijk2023[3:6]

    HuizenPerInwoner2022 = dict()
    for i in range(len(dfOplossing2022)):   
        tijdelijk2022 = dfOplossing2022.loc[i].tolist()
        HuizenPerInwoner2022[tijdelijk2022[1]] = tijdelijk2022[3:6]
        
    DubbeleMensenVan2022en2023 = list()
    for i in HuizenPerInwoner2023:
        for j in HuizenPerInwoner2022:
            for k in range(0,2):
                for l in range(0,2):
                    if HuizenPerInwoner2023[i][k] == HuizenPerInwoner2022[j][l]:
                        if HuizenPerInwoner2023[i][k] not in DubbeleMensenVan2022en2023:
                            DubbeleMensenVan2022en2023.append(HuizenPerInwoner2023[i][k])
                            countTafelburen2022 += 3
    return countTafelburen2022 
                      
    


def Tafelburen2021():
    """
    Controleert of er deelnemers zijn die in zowel 2021 als 2023 naast elkaar aan tafel zitten en kent strafpunten toe.

    De functie laadt de oplossingen voor 2021 en 2023, en voert vervolgens enkele bewerkingen uit op de kolommen.
    Vervolgens worden de huizen per inwoner bepaald. Als een deelnemer in zowel 2021 als 2023 naast dezelfde persoon aan tafel
    zit, worden strafpunten toegekend.

    Returns:
        int: Het totaal aantal strafpunten voor deelnemers die in zowel 2021 als 2023 naast elkaar aan tafel zitten.
    """
    countTafelburen2021 = 0
    dfOplossing2023 = pd.read_excel('Running Dinner eerste oplossing 2023 v2.xlsx')
    dfOplossing2021 = pd.read_excel('Running Dinner eerste oplossing 2021 - corr.xlsx')

    columns_to_add_underscore = ['Voor', 'Hoofd', 'Na']

    for column in columns_to_add_underscore:
        dfOplossing2021[column] = dfOplossing2021[column].apply(lambda x: x[0] + '_' + x[1:] if len(x) > 1 and x[0].isalpha() else x)
    

    for column in columns_to_add_underscore:
        for i in range(len(dfOplossing2023)):
            if dfOplossing2023[column][i][0] == 'W':
                dfOplossing2023[column][i] = dfOplossing2023[column][i][0] + 'O' +dfOplossing2023[column][i][2:]
            elif dfOplossing2023[column][i][0] == "V":
                dfOplossing2023[column][i] = dfOplossing2023[column][i][0] + 'W' +dfOplossing2023[column][i][2:]
    ## kijken welke mensen in welk huis zaten per gang. lijst met unique huizen maken en mensen aan huizen toevoegen.
    ## Dit voor 2022 en 2023 doen. Als er 1 overeen komt, 1 strafpunt erbij
    HuizenPerInwoner2023 = dict()
    for i in range(len(dfOplossing2023)):   
        tijdelijk2023 = dfOplossing2023.loc[i].tolist()
        HuizenPerInwoner2023[tijdelijk2023[1]] = tijdelijk2023[3:6]

    HuizenPerInwoner2021 = dict()
    for i in range(len(dfOplossing2021)):   
        tijdelijk2021 = dfOplossing2021.loc[i].tolist()
        HuizenPerInwoner2021[tijdelijk2021[1]] = tijdelijk2021[3:6]
        
    DubbeleMensenVan2021en2023 = list()
    for i in HuizenPerInwoner2023:
        for j in HuizenPerInwoner2021:
            for k in range(0,2):
                for l in range(0,2):
                    if HuizenPerInwoner2023[i][k] == HuizenPerInwoner2021[j][l]:
                        if HuizenPerInwoner2023[i][k] not in DubbeleMensenVan2021en2023:
                            DubbeleMensenVan2021en2023.append(HuizenPerInwoner2023[i][k])
                            countTafelburen2021 += 1
    return countTafelburen2021



def TafelburenGeenEchteBuren():
    """
    Controleert de burenrelaties van deelnemers en bepaalt of ze naast elkaar aan tafel zitten.

    De functie laadt de oplossing voor 2023, de dataset met bureninformatie en de dataset met bewonersinformatie. Vervolgens
    wordt een mapping gemaakt van bewoners naar hun huisadressen en toegepast op de bureninformatie. Het resultaat wordt
    in een nieuw DataFrame samengevoegd en geprint.

    Returns:
        None
    """
    dfOplossing2023 = pd.read_excel('Running Dinner eerste oplossing 2023 v2.xlsx')
    dfBurenNormaal = pd.read_excel("Running Dinner dataset 2023 v2.xlsx", sheet_name='Buren').drop(0)
    dfBurenNormaal.rename(columns={'De volgende bewoners zijn directe buren': 'Bewoner1', "Unnamed: 1":"Bewoner2"}, inplace=True)
    dfMensenNaarHuizen = pd.read_excel("Running Dinner dataset 2023 v2.xlsx", sheet_name='Bewoners').drop(['Kookt niet'], axis=1).reset_index(drop=True)



    mapping = dfMensenNaarHuizen.set_index('Bewoner')['Huisadres'].to_dict()

    # Apply the mapping to df2 to get the corresponding Huisadres
    dfBurenNormaal['Huisadres1'] = dfBurenNormaal['Bewoner1'].map(mapping)
    dfBurenNormaal['Huisadres2'] = dfBurenNormaal['Bewoner2'].map(mapping)

    # Merge the columns to get the final DataFrame
    result_df = pd.concat([dfBurenNormaal['Bewoner1'], dfBurenNormaal['Bewoner2'], dfBurenNormaal['Huisadres1'], dfBurenNormaal['Huisadres2']], axis=1)
    result_df.columns = ['Bewoner1', 'Bewoner2', 'Huisadres1', 'Huisadres2']
    
    print(result_df)


    dfVoorgerechtMensTussen = pd.DataFrame(dfOplossing2023[['Bewoner']])
    help = pd.DataFrame(dfOplossing2023['Voor'])
    dfVoorgerechtMens = dfVoorgerechtMensTussen.merge(help, left_on="Bewoner")
    print(dfVoorgerechtMens)

    # buur_dict= {}
    # # Loop door de rijen van de DataFrame
    # for index, row in dfBurenNormaal.iterrows():
    #     bewoner1 = row['Bewoner1']
    #     bewoner2 = row['Bewoner2']
    #     adres1 = row['Huisadres1']
    #     adres2 = row['Huisadres2']
    # # Voeg bewoner2 toe aan de lijst van buren van bewoner1
    #     if bewoner1 in buur_dict:
    #         buur_dict[bewoner1].append(adres1)
    #     else:
    #         buur_dict[bewoner1] = [adres2]

    # print((buur_dict.values()))
    # for i in range(1, len(dfMensenNaarHuizen)):
    #     gesjouwvoordict =  dfMensenNaarHuizen.loc[i][1]

    # print(dfBurenNormaal)

    # # for i in buur_dict:
    # #     buur_dict[i] = 
    # # print(dfOplossing2023)
    # # for i in dfOplossing2023['Bewoner']:
    # #     for j in range(0,2):
    # #         if i[j+3] in buur_dict[i]:


def HoofdgerechtVorigJaar():
    """
    Controleert of deelnemers die vorig jaar het hoofdgerecht kookten, dit jaar ook het hoofdgerecht koken.

    De functie laadt de oplossingen voor zowel 2022 als 2023, en bepaalt welke deelnemers vorig jaar het hoofdgerecht kookten.
    Vervolgens wordt gecontroleerd of deze deelnemers dit jaar ook het hoofdgerecht koken. Strafpunten worden toegekend
    voor deelnemers die dit jaar niet het hoofdgerecht koken, maar vorig jaar wel.

    Returns:
        int: Het totaal aantal strafpunten voor deelnemers die vorig jaar het hoofdgerecht kookten, maar dit jaar niet.
    """
    dfOplossing2023 = pd.read_excel('Running Dinner eerste oplossing 2023 v2.xlsx')
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
    dubbelhoofdhuizen = list()
    for i in hoofdgerechtchefs2022:
        for j in hoofdgerechtchefs2023:
            if i in j:
                dubbelhoofdhuizen.append(i)
    dubbelhuizen = list()
    for i in dubbelhoofdhuizen:
        for j in dubbelhoofdhuizen:
            if i[0:5] == j[0:5]:
                dubbelhuizen.append(i[0:5])

    countHoofdgerechtVorigJaar = (len(set(dubbelhuizen)))*5
    return countHoofdgerechtVorigJaar

# HoofdgerechtVorigJaar()
# #TafelburenGeenEchteBuren()
# Tafelburen2021()   
# Tafelburen2022()
# Voorkeursgang()

ExcelFile = 'Running Dinner eerste oplossing 2023 v2.xlsx'
ExcelData = 'Running Dinner dataset 2023 v2.xlsx'

#Twee verschillende deelnemers zijn zo weinig mogelijk keer elkaars tafelgenoten; het liefst
#maximaal één keer. Dit geldt zeker voor deelnemers uit hetzelfde huishouden.

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
    
    def maak_bewoners_dict(df, kolomnaam):
        """
        Maakt een dictionary waarin adressen als keys worden opgeslagen en
        de lijsten van bewoners op dat adres als values.

        Args:
            df : Het DataFrame met de gegevens.
            kolomnaam (str): De naam van de kolom waar de adressen in staan.

        Returns:
            dict: Een dictionary waarin adressen als keys en lijsten van bewoners als value worden opgeslagen.
        """
        bewoners_dict = {}
        for index, row in df.iterrows():
            bewoner = row['Bewoner']
            adres = row[kolomnaam]
            if adres not in bewoners_dict:
                bewoners_dict[adres] = []
            bewoners_dict[adres].append(bewoner)
        return bewoners_dict
    
    def genereer_bewoners_per_adres(df, bewoners_voor, bewoners_hoofd, bewoners_na):
        """
        Genereert een dictionary waarin elke bewoner als key staat en als value
        een lijst van bewoners die tijdens alle gangen samen aan tafel zitten.

        Args:
            df (pandas.DataFrame): Het DataFrame met de gegevens.
            bewoners_voor (dict): Dictionary met bewoners op basis van voorgerecht.
            bewoners_hoofd (dict): Dictionary met bewoners op basis van hoofdgerecht.
            bewoners_na (dict): Dictionary met bewoners op basis van nagerecht.

        Returns:
            dict: Een dictionary waarin bewoners als keys en lijsten van tafelgenoten als value worden opgeslagen.
        """
        bewoners_per_adres = {}
        for index, row in df.iterrows():
            bewoner = row['Bewoner']
            adres_voor = row['Voor']
            adres_hoofd = row['Hoofd']
            adres_na = row['Na']

            bewoners_voorgerecht = bewoners_voor.get(adres_voor, [])
            bewoners_hoofdgerecht = bewoners_hoofd.get(adres_hoofd, [])
            bewoners_nagerecht = bewoners_na.get(adres_na, [])

            bewoners_alle_gangen = (bewoners_voorgerecht + bewoners_hoofdgerecht + bewoners_nagerecht)
            bewoners_per_adres[bewoner] = bewoners_alle_gangen

        return bewoners_per_adres

    bewoners_voor = maak_bewoners_dict(df, 'Voor')
    bewoners_hoofd = maak_bewoners_dict(df, 'Hoofd')
    bewoners_na = maak_bewoners_dict(df, 'Na')

    count_niet_bij_elkaar = 0

    bewoners_per_adres = genereer_bewoners_per_adres(df, bewoners_voor, bewoners_hoofd, bewoners_na)

    for bewoner, tafelgenoten in bewoners_per_adres.items():
        tafelgenoten = [i for i in tafelgenoten if i != bewoner]

        if len([bewoners for bewoners in tafelgenoten if tafelgenoten.count(bewoners)]) >= 2:
            count_niet_bij_elkaar += 6
    count_niet_bij_elkaar = count_niet_bij_elkaar / 2
    return count_niet_bij_elkaar

    
#niet_bij_elkaar(ExcelFile)

# def totaal_som_strafpunten():
#     """
#     Berekent de totale som van strafpunten door verschillende functies op te roepen en hun resultaten op te tellen.

#     Returns:
#         None
#     """
#     print(HoofdgerechtVorigJaar() + Tafelburen2021() + Tafelburen2022() + Voorkeursgang())

# totaal_som_strafpunten()

def totaal_som_strafpunten(df):
    """
    Berekent de totale som van strafpunten door verschillende functies op te roepen en hun resultaten op te tellen.

    Returns:
        int: De totale som van strafpunten.
    """
    strafpunten_hoofdgerecht_vorig_jaar = HoofdgerechtVorigJaar()
    strafpunten_tafelburen_2021 = Tafelburen2021()
    strafpunten_tafelburen_2022 = Tafelburen2022()
    strafpunten_voorkeursgang = Voorkeursgang()
    strafpunten_niet_bij_elkaar= niet_bij_elkaar(df)
    

    totale_strafpunten = (
        strafpunten_hoofdgerecht_vorig_jaar +
        strafpunten_tafelburen_2021 +
        strafpunten_tafelburen_2022 +
        strafpunten_voorkeursgang +
        strafpunten_niet_bij_elkaar
    )

    return int(totale_strafpunten)
#totaal_som_strafpunten(df)
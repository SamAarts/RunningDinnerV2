
import pandas as pd
import numpy as np 

#Onnodige foutcode verhelpen
pd.options.mode.chained_assignment = None

ExcelDataset = 'Running Dinner dataset 2023 v2.xlsx'
ExcelOplossing2023 = 'Running Dinner eerste oplossing 2023 v2.xlsx'
ExcelOplossing2022 = 'Running Dinner eerste oplossing 2022.xlsx' 
ExcelOplossing2021 = 'Running Dinner eerste oplossing 2021 - corr.xlsx'

def Voorkeursgang(ExcelDataset,ExcelOplossing2023):
    """
    Controleert of de voorkeursgang van de deelnemers overeenkomt met de oplossing.

    De functie leest de Excel-bestanden, verwijdert onnodige kolommen en reset de indices. Vervolgens wordt gecontroleerd of 
    de voorkeursgangen in de dataset overeenkomen met de oplossing. Strafpunten worden toegekend voor elke onjuiste voorkeursgang.

    Returns:
        int: Het totaal aantal strafpunten voor onjuiste voorkeursgangen.
    """
    try:
        # Load the Excel files, drop unnecessary columns, and reset the indices
        dfdataset= pd.read_excel(ExcelDataset, sheet_name='Adressen').drop(['Min groepsgrootte', 'Max groepsgrootte'], axis=1).reset_index(drop=True)
        dfoplossing = pd.read_excel(ExcelOplossing2023)
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
    except Exception as e:
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

def Tafelburen2022(ExcelOplossing2023,ExcelOplossing2022):
    """
    Controleert of er deelnemers zijn die in zowel 2022 als 2023 naast elkaar aan tafel zitten en kent strafpunten toe.

    De functie laadt de oplossingen voor 2022 en 2023, en vervolgens worden de huizen per inwoner bepaald. Als een deelnemer
    in zowel 2022 als 2023 naast dezelfde persoon aan tafel zit, worden strafpunten toegekend.

    Returns:
        int: Het totaal aantal strafpunten voor deelnemers die in zowel 2022 als 2023 naast elkaar aan tafel zitten.
    """
    try:
        countTafelburen2022 = 0
        dfOplossing2023 = pd.read_excel(ExcelOplossing2023)
        dfOplossing2022 = pd.read_excel(ExcelOplossing2022)

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
    except Exception as e:
        countTafelburen2022 = 0
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
                      
def Tafelburen2021(ExcelOplossing2023, ExcelOplossing2021):
    """
    Controleert of er deelnemers zijn die in zowel 2021 als 2023 naast elkaar aan tafel zitten en kent strafpunten toe.

    De functie laadt de oplossingen voor 2021 en 2023, en voert vervolgens enkele bewerkingen uit op de kolommen.
    Vervolgens worden de huizen per inwoner bepaald. Als een deelnemer in zowel 2021 als 2023 naast dezelfde persoon aan tafel
    zit, worden strafpunten toegekend.

    Returns:
        int: Het totaal aantal strafpunten voor deelnemers die in zowel 2021 als 2023 naast elkaar aan tafel zitten.
    """
    try:
        countTafelburen2021 = 0
        dfOplossing2023 = pd.read_excel(ExcelOplossing2023)
        dfOplossing2021 = pd.read_excel(ExcelOplossing2021)

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
    except Exception as e:
        countTafelburen2021 = 0

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

def TafelburenGeenEchteBuren(ExcelOplossing2023,ExcelData):
    """
    Controleert de burenrelaties van deelnemers en bepaalt of ze naast elkaar aan tafel zitten.

    De functie laadt de oplossing voor 2023, de dataset met bureninformatie en de dataset met bewonersinformatie. Vervolgens
    wordt een mapping gemaakt van bewoners naar hun huisadressen en toegepast op de bureninformatie. Het resultaat wordt
    in een nieuw DataFrame samengevoegd en geprint.

    Returns:
        None
    """
    try:  
        dfOplossing = pd.read_excel(ExcelOplossing2023)
        df = pd.read_excel(ExcelData).drop(columns=['Kookt niet']).sort_values(by=['Bewoner'])
        dftijdelijk = pd.read_excel(ExcelData, sheet_name='Buren').drop([0])
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
        return BuurmanCount

def HoofdgerechtVorigJaar(ExcelOplossing2023,ExcelOplossing2022):
    """
    Controleert of deelnemers die vorig jaar het hoofdgerecht kookten, dit jaar ook het hoofdgerecht koken.

    De functie laadt de oplossingen voor zowel 2022 als 2023, en bepaalt welke deelnemers vorig jaar het hoofdgerecht kookten.
    Vervolgens wordt gecontroleerd of deze deelnemers dit jaar ook het hoofdgerecht koken. Strafpunten worden toegekend
    voor deelnemers die dit jaar niet het hoofdgerecht koken, maar vorig jaar wel.

    Returns:
        int: Het totaal aantal strafpunten voor deelnemers die vorig jaar het hoofdgerecht kookten, maar dit jaar niet.
    """
    try:
        dfOplossing2023 = pd.read_excel(ExcelOplossing2023)
        dfOplossing2022 = pd.read_excel(ExcelOplossing2022)

        # Check if the columns exist before dropping them
        columns_to_drop = ['Unnamed: 0', 'Huisadres', 'Voor', 'Hoofd', 'Na', 'aantal']
        dfnieuw2 = dfOplossing2023.drop(columns=[col for col in columns_to_drop if col in dfOplossing2023], errors='ignore')
        dfnieuw = dfOplossing2022.drop(columns=[col for col in columns_to_drop if col in dfOplossing2022], errors='ignore')
        
        hoofdgerechtchefs2022 = list()
        for i in range(len(dfnieuw)):
            if dfnieuw['kookt'][i] == "Hoofd":
                hoofdgerechtchefs2022.append(dfnieuw['Bewoner'][i])

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

    
    except Exception as e:        
        hoofdgerechtchefs2022 = list()
        for i in range(len(dfnieuw)):
            if dfnieuw['kookt'][i] == "Hoofd":
                hoofdgerechtchefs2022.append(dfnieuw['Bewoner'][i])

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

def niet_bij_elkaar(ExcelOplossing2023):
    """
    Deze functie berekent het aantal keren dat bewoners elkaar tegenkomen tijdens verschillende gangen,
    waarbij ze zo min mogelijk bij elkaar aan tafel mogen zitten. Het resultaat is het aantal keren dat dit voorkomt,
    vermenigvuldigd met 6 (dit omdat het een strenge eis is).

    Args:
        ExcelInput (str): De bestandsnaam (en pad) van het Excel-bestand met de tafelindeling.

    Returns:
        int: Het totale aantal keren dat bewoners elkaar tegenkomen en niet bij elkaar mogen zitten, vermenigvuldigd met 6.
    """
    try:
        count_niet_bij_elkaar = 0
        # Lees het Excel-bestand
        df = pd.read_excel(ExcelOplossing2023)
        
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
    except Exception as e:
        count_niet_bij_elkaar = 0
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
 
def totaal_som_strafpunten(ExcelOplossing2023, ExcelOplossing2022):
    """
    Berekent de totale som van strafpunten door verschillende functies op te roepen en hun resultaten op te tellen.

    Returns:
        int: De totale som van strafpunten.
    """

    strafpunten_hoofdgerecht_vorig_jaar = HoofdgerechtVorigJaar(ExcelOplossing2023,ExcelOplossing2022)
    strafpunten_tafelburen_2021 = Tafelburen2021(ExcelOplossing2023, ExcelOplossing2021)
    strafpunten_tafelburen_2022 = Tafelburen2022(ExcelOplossing2023,ExcelOplossing2022)
    strafpunten_voorkeursgang = Voorkeursgang(ExcelDataset,ExcelOplossing2023)
    strafpunten_niet_bij_elkaar= niet_bij_elkaar(ExcelOplossing2023)
    strafpunten_voor_dineren_met_buurman = TafelburenGeenEchteBuren(ExcelOplossing2023,ExcelDataset)

    totale_strafpunten = (
        strafpunten_hoofdgerecht_vorig_jaar +
        strafpunten_tafelburen_2021 +
        strafpunten_tafelburen_2022 +
        strafpunten_voorkeursgang +
        strafpunten_niet_bij_elkaar +
        strafpunten_voor_dineren_met_buurman
    )

    return print(totale_strafpunten)


totaal_som_strafpunten(ExcelOplossing2023, ExcelOplossing2022)









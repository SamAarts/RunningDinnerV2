
import pandas as pd
import numpy as np

def Voorkeursgang():
   

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

    print(countVoorkeursgang)
        

## hij print welk gerecht hij wel doet
# Voorkeursgang()

def Tafelburen2022():
    countTafelburen2022 = 0
    dfOplossing2023 = pd.read_excel('Running Dinner eerste oplossing 2023 v2.xlsx')
    dfOplossing2022 = pd.read_excel('Running Dinner eerste oplossing 2022.xlsx')

    dfOplossing2022['Voor'] = dfOplossing2022['Voor'].str.replace(r'(\d+)', r'_\1')
    dfOplossing2022['Hoofd'] = dfOplossing2022['Hoofd'].str.replace(r'(\d+)', r'_\1')
    dfOplossing2022['Na'] = dfOplossing2022['Na'].str.replace(r'(\d+)', r'_\1')
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
    print(DubbeleMensenVan2022en2023) 
    countTafelburen2022 += 3                  
    


def Tafelburen2021():
    countTafelburen2022 = 0
    dfOplossing2023 = pd.read_excel('Running Dinner eerste oplossing 2023 v2.xlsx')
    dfOplossing2021 = pd.read_excel('Running Dinner eerste oplossing 2021 - corr.xlsx')

    columns_to_add_underscore = ['Voor', 'Hoofd', 'Na']

    for column in columns_to_add_underscore:
        dfOplossing2021[column] = dfOplossing2021[column].apply(lambda x: x[0] + '_' + x[1:] if len(x) > 1 and x[0].isalpha() else x)
    

    for column in columns_to_add_underscore:
        for i in range(len(dfOplossing2023)):
            if dfOplossing2023[column][i][0] == 'W':
                dfOplossing2023[column][i] = dfOplossing2023[column][i][0] + 'O' +dfOplossing2023[column][i][0:]
            elif dfOplossing2023[column][i][0] == "V":
                dfOplossing2023[column][i] = dfOplossing2023[column][i][0] + 'W' +dfOplossing2023[column][i][0:]
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
    print(dfOplossing2021, dfOplossing2023)
    countTafelburen2022 += 1

Tafelburen2021()   
#Tafelburen2022()
# Voorkeursgang()


# Twee verschillende deelnemers zijn zo weinig mogelijk keer elkaars tafelgenoten; het liefst
# maximaal één keer. Dit geldt zeker voor deelnemers uit hetzelfde huishouden


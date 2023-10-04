
import pandas as pd
import numpy as np

#Onnodige foutcode verhelpen
pd.options.mode.chained_assignment = None

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

    return  countVoorkeursgang
        

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
                            countTafelburen2022 += 3
    return countTafelburen2022 
                      
    


def Tafelburen2021():
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

def totaal_som_strafpunten():
    print(HoofdgerechtVorigJaar() + Tafelburen2021() + Tafelburen2022() + Voorkeursgang())

totaal_som_strafpunten()

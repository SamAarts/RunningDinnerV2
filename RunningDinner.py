import pandas as pd
import numpy as np
import math

#Geef hier de naam van de nieuwe excel database op:
ExcelInput = 'Running Dinner dataset 2022.xlsx'


#Hier gaan we de excel tabbladen naar verschillende DataFrames inlezen.
dfBewoners = pd.read_excel(ExcelInput, sheet_name='Bewoners')
dfAdressen = pd.read_excel(ExcelInput, sheet_name='Adressen')
dfPaarBlijftBijElkaar = pd.read_excel(ExcelInput, sheet_name='Paar blijft bij elkaar')
dfBuren = pd.read_excel(ExcelInput, skiprows=[0], sheet_name='Buren')
dfKookteVorigJaar = pd.read_excel(ExcelInput, skiprows=[0], sheet_name='Kookte vorig jaar')
dfTafelGenootVorigJaar = pd.read_excel(ExcelInput, skiprows=[0], sheet_name='Tafelgenoot vorig jaar')

#Hier gaan we de apparte dataFrames bewerken zodat ze makkelijker te behandelen zijn.
#We gaan string slicen op adressen zodat we ze later kunnen toevoegen aan de juiste bewoners
for i in range(len(dfKookteVorigJaar['Huisadres'])):
    dfKookteVorigJaar.loc[i, 'Huisadres'] = dfKookteVorigJaar['Huisadres'][i][0:2] + '_' + dfKookteVorigJaar['Huisadres'][i][2:]


#Hier gaan we de verschillende dataframes samenvoegen tot 1 enkele dataframe
df = dfBewoners.merge(dfAdressen, how = 'left', on ='Huisadres')




#Zorgen dat de lijst met huisadressen hetzelfde is als de lijst met personen. Dit om later makkelijker te kunnen slicen. String slicen
for i in range(len(df['Huisadres'])):
    df.loc[i, 'Huisadres'] = df['Huisadres'][i][0:2] + '_' + df['Huisadres'][i][2:]


#Een lijst maken zodat er later een extra colom kan worden toegevoegd aan de dataframe om te zien of er mensen bij elkaar moeten blijven of niet. 
Bijelkaarbinairlijst = list()
for i in range(len(df['Huisadres'])):
    if df['Huisadres'][i] == 'WO_59' or df['Huisadres'][i] == 'WO_25':
        Bijelkaarbinairlijst.append(1)
    elif df['Huisadres'][i] != 'WO_59' and df['Huisadres'][i] != 'WO_25':
        Bijelkaarbinairlijst.append(0)

#De colom maken om te kunnen visualiseren welke personen er bij iemand moeten blijven
df['Koppel blijft bijelkaar'] = Bijelkaarbinairlijst

#Verzamelingen definieren
Huisadres = df['Huisadres']
Deelnemers = df['Bewoner']

#Proberen om de gangen in de grote dataframe te krijgen
df = df.merge(dfKookteVorigJaar, how = 'left', on ='Huisadres')
df.columns = ['Bewoner','Huisadres','Kookt niet','Min groepsgrootte', 'Max groepsgrootte','Voorkeur gang', 'Koppel blijft bijelkaar', 'Vorig jaar gang']


df.to_excel('Output.xlsx')  
print(df)

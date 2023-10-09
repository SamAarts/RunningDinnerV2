import pandas as pd
import numpy as np

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
        dftijdelijk = pd.read_excel('Running Dinner dataset 2023 v2.xlsx', sheet_name='Buren').drop([0])
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

df = pd.read_excel("Running Dinner eerste oplossing 2023 v2.xlsx")
print(TafelburenGeenEchteBuren(df))
import pandas as pd
import numpy as np

df = pd.read_excel('Running Dinner eerste oplossing 2023 v2.xlsx')
## wie eet welke gang in welk huis
def Mensen_Per_Huis(df):
    huizenvoor = dict()
    huisadressen = list()
    for i in range(len(df)):
        if isinstance(df.loc[i]['kookt'], str):
            huisadressen.append(df.loc[i]['Huisadres'])

    huizenuniek = np.unique(huisadressen)
    for i in huizenuniek:
        tijdelijk = list()
        for j in range(len(df)):
            if df.loc[j]['Voor'] == i:
                tijdelijk.append(df.loc[j]["Bewoner"])

        if len(tijdelijk) > 0:
            huizenvoor[i] = tijdelijk

    return huizenvoor
print(Mensen_Per_Huis(df))
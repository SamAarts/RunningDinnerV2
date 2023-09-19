import pandas as pd
import numpy as np

#Geef hier de nieuwe input op

ExcelInput = 'Running Dinner dataset 2022.xlsx'
# read excel
df = pd.read_excel(ExcelInput, sheet_name='Bewoners')


A = df['Huisadres']
print(df)
# k_a = 1 als de deelnemer wonend op huisadres a vrijgesteld is van koken, 0 anders

k_a = []
for a in A:
    print(a)
    if df['Kookt niet'] == True:
        k_a.append(True)
    else:
        k_a.append(False)
print(k_a)
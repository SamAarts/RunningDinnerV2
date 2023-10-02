

def Voorkeursgang():
    import pandas as pd

    # Load the Excel files, drop unnecessary columns, and reset the indices
    df2022 = pd.read_excel('Running Dinner dataset 2022.xlsx', sheet_name='Adressen').drop(['Min groepsgrootte', 'Max groepsgrootte'], axis=1).reset_index(drop=True)
    df2021 = pd.read_excel('Running Dinner dataset 2021.xlsx', sheet_name='Adressen').drop(['Min groepsgrootte', 'Max groepsgrootte'], axis=1).reset_index(drop=True)
    df = df2021.merge(df2022)


    print(df)


Voorkeursgang()
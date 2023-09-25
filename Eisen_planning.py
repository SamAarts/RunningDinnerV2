import pandas as pd
import numpy as np

# 
def controleer_gangen(ExcelInput):
    # Lees het Excel-bestand
    df = pd.read_excel(ExcelInput)

    # Kopieer het dataframe zodat het origineel behouden blijft
    df_new = df.copy()

    def controleer_gang(gang_naam):
        ontbrekende_gang = df[df[gang_naam].isnull()]

        if ontbrekende_gang.empty:
            print(f'iedereen krijgt {gang_naam} gerecht')
        else:
            personen_zonder_gang = ontbrekende_gang['Bewoner'].tolist()
            print(f"Aantal mensen die geen {gang_naam} gerecht krijgen:", len(personen_zonder_gang))
            if len(personen_zonder_gang) > 0:
                print(f"Deze personen hebben geen {gang_naam}gerecht:")
                print(personen_zonder_gang)

    # Roep de functie aan voor verschillende gangen
    controleer_gang('Voor')
    controleer_gang('Hoofd')
    controleer_gang('Na')

# Roep de functie aan met het pad naar je Excel-bestand als argument
controleer_gangen('Running Dinner eerste oplossing 2022.xlsx')

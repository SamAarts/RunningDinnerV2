import random
import logging
import copy
import pandas as pd

# importeer alle functies?
# eisen:
from Eisen_planning import controleer_gangen
from Eisen_planning import iedereen_een_gang
from Eisen_planning import huisadressen_niet_koken
from Eisen_planning import deelnemers_op_huisadres
from Eisen_planning import paren_bij_elkaar
# wensen:
from Wensen_planning import Voorkeursgang
from Wensen_planning import Tafelburen2022
from Wensen_planning import Tafelburen2021
from Wensen_planning import TafelburenGeenEchteBuren
from Wensen_planning import HoofdgerechtVorigJaar
from Wensen_planning import niet_bij_elkaar
from Wensen_planning import totaal_som_strafpunten



ExcelDataset = 'Running Dinner dataset 2023 v2.xlsx'
ExcelOplossing2023 = 'Running Dinner eerste oplossing 2023 v2.xlsx'
ExcelOplossing2022 = 'Running Dinner eerste oplossing 2022.xlsx' 
ExcelOplossing2021 = 'Running Dinner eerste oplossing 2021 - corr.xlsx'

def two_opt(ExcelOplossing2023):
    # Read the Excel file into a DataFrame
    df = pd.read_excel(ExcelOplossing2023)
    
    # Perform the Two-Opt optimization
    improved = True
    while improved:
        improved = False
        totale_strafpunten = totaal_som_strafpunten(df)  # Ensure totale_som_strafpunten accepts a file path
        if totale_strafpunten is not None:
            logger.debug(f"Totale aantal strafpunten: {totale_strafpunten}")
            i = 1
            while (i <= len(df) - 2) and not improved:
                j = i + 1
                while (j < len(df)) and not improved:
                    # Verwissel waarden in kolom 'Voor'
                    df.loc[i, 'Voor'], df.loc[j, 'Voor'] = df.loc[j, 'Voor'], df.loc[i, 'Voor']
                    if j - i == 1:
                        j += 1
                        continue
                    new_strafpunten = copy.copy(totale_strafpunten)
                    # new_strafpunten[i:j] = reversed(totale_strafpunten[i:j])
                    totale_new_strafpunten = totaal_som_strafpunten(df)  # Ensure totaal_som_strafpunten accepts a file path
                    if totale_new_strafpunten < totale_strafpunten:
                        logger.debug(f"New strafpunten has total value: {totale_new_strafpunten}, so: Improvement for i,j={i},{j}")
                        totale_strafpunten = new_strafpunten
                        logger.debug(f"Strafpunten updated: tour={new_strafpunten}")
                        improved = True
                    else:
                        logger.debug(f"New strafpunten has total value: {totale_new_strafpunten}, so: No improvement for i,j={i},{j}")
                    j += 1
                i += 1
    return totale_strafpunten

two_opt(ExcelOplossing2023)  # Make sure ExcelOplossing2023 contains the correct file path

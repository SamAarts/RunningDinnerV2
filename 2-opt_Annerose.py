import random
import logging
import copy
import pandas as pd
import itertools
import importlib
import sys
from collections import defaultdict
sys.path.append('code/')
from Wensen_planning import *

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

logger = logging.getLogger(name='2opt-logger')
logging.basicConfig(level=logging.DEBUG,
                    format='[%(asctime)s] %(message)s',
                    handlers=[logging.FileHandler("2-opt_debug-Sam.log")])

importlib.reload(sys.modules['Wensen_planning'])
def two_opt(ExcelInput):
    df = pd.read_excel(ExcelInput)   
    dfcopy = df.copy()
    improved = True
    totale_strafpunten = totaal_som_strafpunten(df)

    new_strafpunten = totale_strafpunten

    while improved:
        improved = False
        logger.debug(f"Totale aantal strafpunten: {totale_strafpunten}") 
        
        for k in range(3):
            gangen = ['Voor', "Hoofd", "Na"]
            numbers = list(itertools.chain(range(0, len(df))))
            random.shuffle(numbers)
            for i in (numbers):
                logger.debug(f"update i: {i}")
                random.shuffle(numbers)
                for j in numbers:
                    gang_verandering = random.choice(gangen)
                    if gang_verandering == dfcopy.loc[i,'kookt']:
                        new_strafpunten_copy = totaal_som_strafpunten(dfcopy) 
                        continue
                    else:
                        dfcopy.loc[i, gang_verandering], dfcopy.loc[j, gang_verandering] = dfcopy.loc[j, gang_verandering], dfcopy.loc[i, gang_verandering]
                        new_strafpunten_copy = totaal_som_strafpunten(dfcopy)                  
                    if new_strafpunten_copy < totale_strafpunten:
                        new_strafpunten = new_strafpunten_copy
                        totale_strafpunten = new_strafpunten
                        df = dfcopy
                        improved = True
                        print("df heeft geupdate")  
                        df.to_excel("Output.xlsx")  
                        logger.debug(f"Strafpunten has total value: {totale_strafpunten}, i,j={i},{j}")             
        i += 1
    return totale_strafpunten

ExcelFile = 'Running Dinner eerste oplossing 2023 v2.xlsx'
two_opt(ExcelFile)



import pandas as pd

ExcelFile = 'Running Dinner eerste oplossing 2022.xlsx'
ExcelData = 'Running Dinner dataset 2022.xlsx'

#Twee verschillende deelnemers zijn zo weinig mogelijk keer elkaars tafelgenoten; het liefst
#maximaal één keer. Dit geldt zeker voor deelnemers uit hetzelfde huishouden.

def niet_bij_elkaar(ExcelInput):
    """
    Deze functie berekent het aantal keren dat bewoners elkaar tegenkomen tijdens verschillende gangen,
    waarbij ze zo min mogelijk bij elkaar aan tafel mogen zitten. Het resultaat is het aantal keren dat dit voorkomt,
    vermenigvuldigd met 6 (dit omdat het een strenge eis is).

    Args:
        ExcelInput (str): De bestandsnaam (en pad) van het Excel-bestand met de tafelindeling.

    Returns:
        int: Het totale aantal keren dat bewoners elkaar tegenkomen en niet bij elkaar mogen zitten, vermenigvuldigd met 6.
    """
    count_niet_bij_elkaar = 0
    # Lees het Excel-bestand
    df = pd.read_excel(ExcelInput)
    
    def maak_bewoners_dict(df, kolomnaam):
        """
        Maakt een dictionary waarin adressen als keys worden opgeslagen en
        de lijsten van bewoners op dat adres als values.

        Args:
            df : Het DataFrame met de gegevens.
            kolomnaam (str): De naam van de kolom waar de adressen in staan.

        Returns:
            dict: Een dictionary waarin adressen als keys en lijsten van bewoners als value worden opgeslagen.
        """
        bewoners_dict = {}
        for index, row in df.iterrows():
            bewoner = row['Bewoner']
            adres = row[kolomnaam]
            if adres not in bewoners_dict:
                bewoners_dict[adres] = []
            bewoners_dict[adres].append(bewoner)
        return bewoners_dict
    
    def genereer_bewoners_per_adres(df, bewoners_voor, bewoners_hoofd, bewoners_na):
        """
        Genereert een dictionary waarin elke bewoner als key staat en als value
        een lijst van bewoners die tijdens alle gangen samen aan tafel zitten.

        Args:
            df (pandas.DataFrame): Het DataFrame met de gegevens.
            bewoners_voor (dict): Dictionary met bewoners op basis van voorgerecht.
            bewoners_hoofd (dict): Dictionary met bewoners op basis van hoofdgerecht.
            bewoners_na (dict): Dictionary met bewoners op basis van nagerecht.

        Returns:
            dict: Een dictionary waarin bewoners als keys en lijsten van tafelgenoten als value worden opgeslagen.
        """
        bewoners_per_adres = {}
        for index, row in df.iterrows():
            bewoner = row['Bewoner']
            adres_voor = row['Voor']
            adres_hoofd = row['Hoofd']
            adres_na = row['Na']

            bewoners_voorgerecht = bewoners_voor.get(adres_voor, [])
            bewoners_hoofdgerecht = bewoners_hoofd.get(adres_hoofd, [])
            bewoners_nagerecht = bewoners_na.get(adres_na, [])

            bewoners_alle_gangen = (bewoners_voorgerecht + bewoners_hoofdgerecht + bewoners_nagerecht)
            bewoners_per_adres[bewoner] = bewoners_alle_gangen

        return bewoners_per_adres

    bewoners_voor = maak_bewoners_dict(df, 'Voor')
    bewoners_hoofd = maak_bewoners_dict(df, 'Hoofd')
    bewoners_na = maak_bewoners_dict(df, 'Na')

    count_niet_bij_elkaar = 0

    bewoners_per_adres = genereer_bewoners_per_adres(df, bewoners_voor, bewoners_hoofd, bewoners_na)

    for bewoner, tafelgenoten in bewoners_per_adres.items():
        tafelgenoten = [i for i in tafelgenoten if i != bewoner]

        if len([bewoners for bewoners in tafelgenoten if tafelgenoten.count(bewoners)]) >= 2:
            count_niet_bij_elkaar += 6

    return print(count_niet_bij_elkaar / 2)

    
niet_bij_elkaar(ExcelFile)





    

    


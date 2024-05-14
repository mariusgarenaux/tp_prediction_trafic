import pandas as pd
from simplificator.sf_dataframe import SfDataFrame
from simplificator.sf_geodataframe import SfGeoDataFrame
from simplificator.sf_err import MissingColumn
from simplificator.sf_config import CONFIG
import datetime

START_URL = CONFIG["START_URL"]

PATH_TRAIN_BIG_ONLINE = START_URL + CONFIG["PATH_TRAIN_BIG_ONLINE"]
PATH_TRAIN_BIG_LOCAL = CONFIG["PATH_TRAIN_BIG_LOCAL"]

PATH_TRAIN_SMALL_ONLINE = START_URL + CONFIG["PATH_TRAIN_SMALL_ONLINE"]
PATH_TRAIN_SMALL_LOCAL = CONFIG["PATH_TRAIN_SMALL_LOCAL"]

PATH_TRONCON_ONLINE = START_URL + CONFIG["PATH_TRONCON_ONLINE"]
PATH_TRONCON_LOCAL = CONFIG["PATH_TRONCON_LOCAL"]

PATH_CURRENT_ONLINE = CONFIG["PATH_CURRENT_ONLINE"]
PATH_CURRENT_LOCAL = CONFIG["PATH_CURRENT_LOCAL"]

DICT_TRAD_ETAT_TRAFIC = CONFIG["DICT_TRAD_ETAT_TRAFIC"]
DICT_ETAT_TRAFIC_TO_COLOR = CONFIG["DICT_ETAT_TRAFIC_TO_COLOR"]
DICT_TRAD_JOUR = CONFIG["DICT_TRAD_JOUR"]
USECOLS_SF = CONFIG["USECOLS_SF"]
USECOLS_OD = CONFIG["USECOLS_OD"]
USECOLS_OD_2 = CONFIG["USECOLS_OD_2"]
DICT_OD_SF = CONFIG["DICT_OD_SF"]
DICT_OD_SF_2 = CONFIG["DICT_OD_SF_2"]

def load_data(path_local, path_online, columns):
    try:
        df = pd.read_csv(path_online, sep=";", usecols=columns)
    
    except Exception as e:
        df = load_local_data(path_local, columns)
    return df

def load_local_data(path, columns):
    try:
        df = pd.read_csv(path, sep=";", usecols=columns)
    except Exception as e:
        raise e
    else:
        print("online file not found, local file was loaded")
        return df

def charger_donnees_troncon():
    """
    Creates a SfGeoDataFrame with traffic data from PATH_TRONCON. Supposed to be information about roads of Rennes.
    :return: a SfGeoDataFrame with traffic data. Columns are 'id_troncon', 'hierarchie', 'denomination'.
    """
    df = load_data(PATH_TRONCON_LOCAL, PATH_TRONCON_ONLINE, ['id_troncon', 'hierarchie', 'denomination'])
    sdf = SfDataFrame(df)
    print("Les données ont bien été chargées.")
    return sdf

def charger_donnees_trafic_1():
    """
    Creates a SfGeoDataFrame with traffic data from PATH_TRAIN_SMALL. Supposed to be a small training set.
    :return: a SfGeoDataFrame with traffic data. Columns are 'date_heure', 'etat_trafic', 'id_troncon'.
    """
    df = load_data(PATH_TRAIN_SMALL_LOCAL, PATH_TRAIN_SMALL_ONLINE, ['jour', 'heure', 'etat_trafic', 'id_troncon'])
    sdf = SfDataFrame(df)
    print("Les données ont bien été chargées.")
    return sdf

def charger_donnees_trafic_2():
    """
    Creates a SfGeoDataFrame with traffic data from PATH_TRAIN_SMALL. Supposed to be a small training set.
    :return: a SfGeoDataFrame with traffic data. Columns are USECOLS_OD.
    """
    df = load_data(PATH_TRAIN_SMALL_LOCAL, PATH_TRAIN_SMALL_ONLINE, USECOLS_SF)
    sgdf = SfGeoDataFrame(df = df, hidden_columns=['geojson'], geometry='geojson')
    return sgdf

def charger_donnees_trafic_3(custom_uuid:str = CONFIG["PATH_TRAIN_BIG_ONLINE"]):
    """
    Creates a SfGeoDataFrame with traffic data from PATH_TRAIN_BIG. Supposed to be a big training set. If 
    :return: a SfGeoDataFrame with traffic data. Columns are USECOLS_OD.
    """
    path_train_big_online = START_URL + custom_uuid
    df = load_data(PATH_TRAIN_BIG_LOCAL, path_train_big_online, USECOLS_SF)
    sgdf = SfGeoDataFrame(df = df, hidden_columns=['geojson'], geometry='geojson')
    return sgdf

def charger_donnees_trafic_actuel():
    """
    Creates a SfGeoDataFrame with current traffic data from Rennes.
    :return: a SfGeoDataFrame with traffic data. Columns are USECOLS_OD.
    """
    usecols_online = USECOLS_OD
    dict_od_sf = DICT_OD_SF
    try:
        pd.read_csv(PATH_CURRENT_ONLINE, sep=";", usecols=usecols_online)
    except ValueError:
        usecols_online = USECOLS_OD_2
        dict_od_sf = DICT_OD_SF_2
    df = load_data(PATH_CURRENT_LOCAL, PATH_CURRENT_ONLINE, usecols_online)
    df = df.rename(columns=dict_od_sf)
    df = df.loc[df['etat_trafic'] != 'unknown']
    df = datetime_to_jour_heure(df)
    sgdf = SfGeoDataFrame(df = df, hidden_columns=['geojson'], geometry='geojson')
    sgdf.change_column('etat_trafic', DICT_TRAD_ETAT_TRAFIC)
    return sgdf

def datetime_to_jour_heure(df: pd.DataFrame) -> pd.DataFrame:
    """
    Changes one column of df containing date in iso format to two columns. First is the day, second is the hour.
    :return: df, with the column 'date_heure' removed and the columns 'jour' and 'hour' added.
    """
    df_new = df.copy()
    df_new['date'] = [datetime.datetime.fromisoformat(x) for x in df_new['date_heure']]
    df_new = df_new.drop('date_heure', axis=1)
    df_new['jour'] = [DICT_TRAD_JOUR[date.strftime('%A')] for date in df_new['date']]
    df_new['heure'] = [date.hour for date in df_new['date']]
    return  df_new.drop('date', axis = 1)

def nouveau_tableau(lignes: list[list], colonnes: list[str]) -> SfDataFrame:
    """
    Creates a new SfDataFrame from a matrix and column names.
    :param lignes: an array of array(s), that must have the same length.
    :param colonnes: the names of the columns.
    :return: a SfDataFrame with data from lignes.
    """
    df = pd.DataFrame(lignes, columns=colonnes)
    return SfDataFrame(df = df)

def rajouter_couleur_depuis_etat_trafic(sdf: SfGeoDataFrame):
    """
    Specification of SfGeoDataFrame rajouter_couleur, when there is a column named 'etat_trafic' with values from DICT_ETAT_TRAFIC_TO_COLOR.
    """
    if 'etat_trafic' not in sdf.df.columns:
        raise MissingColumn('etat_trafic')
        
    values = sdf.df['etat_trafic'].unique()
    for value in values :
        if value not in DICT_ETAT_TRAFIC_TO_COLOR:
            raise KeyError(f"{value} not in {DICT_ETAT_TRAFIC_TO_COLOR}")
        
    sdf.rajouter_couleur(column_from='etat_trafic', d = DICT_ETAT_TRAFIC_TO_COLOR)

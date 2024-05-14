CONFIG = {
    "START_URL": "https://bacasable.fenix.rudi-univ-rennes1.fr/media/download",

    "PATH_TRAIN_BIG_ONLINE": "/6b610a3f-418f-490b-a46a-205d2ba44647",
    "PATH_TRAIN_BIG_LOCAL": "./data/traffic_big.csv",

    "PATH_TRAIN_SMALL_ONLINE": "/e328e2a2-2e66-40ce-91c9-03cfbbeb53a1",
    "PATH_TRAIN_SMALL_LOCAL" : "./data/traffic_small.csv",

    "PATH_TRONCON_ONLINE" : "/04c0fa7c-0a72-4689-b950-cef2811302e2",
    "PATH_TRONCON_LOCAL" : "./data/troncons_rennes.csv",
    "PATH_CURRENT_ONLINE" : "https://data.rennesmetropole.fr/api/explore/v2.1/catalog/datasets/etat-du-trafic-en-temps-reel/exports/csv?lang=fr&timezone=Europe%2FBerlin&use_labels=true&delimiter=%3B",
    "PATH_CURRENT_LOCAL" : "./data/traffic_current.csv",

    "DICT_TRAD_ETAT_TRAFIC" : {
        "impossible": "circulation_impossible", 
        "congested": "tres_ralenti",
        "heavy": "ralenti", 
        "freeFlow": "fluide",
        "unknown": "inconnu"
    },
    "DICT_ETAT_TRAFIC_TO_COLOR" : {
        "circulation_impossible": "red", 
        "tres_ralenti": "orange",
        "ralenti": "yellow", 
        "fluide": "green",
        "inconnu": "grey"
    },
    "DICT_TRAD_JOUR" : {
        "Monday": "lundi",
        "Tuesday": "mardi",
        "Wednesday": "mercredi",
        "Thursday": "jeudi",
        "Friday": "vendredi",
        "Saturday": "samedi",
        "Sunday": "dimanche"
    },
    "USECOLS_SF" : ["jour", "heure", "etat_trafic", "id_troncon", "geojson", "coordonnees", "denomination", "hierarchie"],
    "USECOLS_OD" : ["datetime", "trafficStatus", "predefinedLocationReference", "Geo Shape", "Geo Point", "denomination", "hierarchie"],
    "USECOLS_OD_2": ["datetime", "trafficstatus", "predefinedlocationreference", "geo_shape", "geo_point_2d", "denomination", "hierarchie"],
    "DICT_OD_SF" : {
        "datetime": "date_heure",
        "trafficStatus": "etat_trafic",
        "predefinedLocationReference": "id_troncon",
        "Geo Shape": "geojson",
        "Geo Point": "coordonnees",
        "denomination": "denomination",
        "hierarchie": "hierarchie"
    },
    "DICT_OD_SF_2" : {
        "datetime": "date_heure",
        "trafficstatus": "etat_trafic",
        "predefinedlocationreference": "id_troncon",
        "geo_shape": "geojson",
        "geo_point": "coordonnees",
        "denomination": "denomination",
        "hierarchie": "hierarchie"
    }

}
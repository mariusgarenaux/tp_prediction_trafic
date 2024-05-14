import pandas as pd
import numpy as np
import folium
import json

from simplificator.sf_dataframe import SfDataFrame
from simplificator.sf_err import MissingColumn, MissingRow, NotMatchIndexes, NoJsonGeometry

def convert_to_json(element):
    if isinstance(element, dict):
        return element
    if type(element) in [float, np.float64, np.float32]:
        return {}
    try:
        json.loads(element)
    except:
        raise NoJsonGeometry(element)
    else:
        return json.loads(element)

class SfGeoDataFrame(SfDataFrame):
    def __init__(self, df: pd.DataFrame, hidden_columns: list[str] = [], geometry: str = None, color: str = None):
        """
        Creates a geopandas GeoDataFrame like. 
        :param hidden_columns: names of columns we don't want to show.
        :param geometry: name of a column of df to use as a geometry column.
        :param color: name of the column of df with color informations.
        """
        super().__init__(df = df, hidden_columns= hidden_columns)
        if geometry not in self.df.columns and geometry is not None:
            raise MissingColumn(geometry)
        if color not in self.df.columns and color is not None:
            raise MissingColumn(color)
        self.geometry = geometry
        self.color = color
        self.set_geometry()

    def set_geometry(self):
        """
        Sets the geometry column's elements to correct json objects, in case geometry columns dtype is strings.
        """
        if (self.df.shape[0] == 0) or (self.geometry not in self.df.columns) :
            return

        self.df[self.geometry] = [convert_to_json(element) for element in self.df[self.geometry]]

    def afficher_sur_une_carte(self) -> folium.Map | None:
        """
        Shows on a folium Map the data from self.df. If self has a geometry column, it uses it.
        If self.color is set, it shows the colors on the map.
        :return: a folium Map with data from self.df.
        """
        if self.geometry is None:
            return None

        m = folium.Map(location = (48.11, -1.65), zoom_start=13)
        geojson = {
            "type": "FeatureCollection",
            "features": [{
                        'type': 'Feature',
                        'geometry': x
                        } for x in self.df[self.geometry].tolist()]
            }
        if self.color is None:
            folium.GeoJson(
                data = geojson,
            ).add_to(m)
            return m

        for k, feature in enumerate(geojson["features"]):
            if isinstance(feature, dict):
                feature[self.color] = self.df[self.color].values[k]
            else:
                feature[self.color] = 'grey'
        folium.GeoJson(
            data = geojson,
            style_function = lambda feature :{
                'color' : feature[self.color]
            }
        ).add_to(m)
        return m

    def sous_tableau(self, lignes: list = [], colonnes: list[str] = []):
        """
        Give a subset of self.df, with rows in lignes an columns in columns.
        :param lignes: the index of the rows we want to put in our subset.
        :param columns: the columns we want to keep in our subset.
        :return: a SfGeoDataFrame, with data being a subset of self.df.
        """
        if not isinstance(lignes, list):
            raise TypeError('lignes doit être une liste')
        if not isinstance(colonnes, list):
            raise TypeError('colonnes doit être une liste')
        for ligne in lignes :
            if ligne not in self.df.index:
                raise MissingRow(ligne)
        for colonne in colonnes :
            if colonne not in self.df.columns:
                raise MissingColumn(colonne)
        
        if len(lignes) == 0:
            lignes = self.df.index
        if len(colonnes) == 0:
            colonnes = list(self.df.columns)
        
        colonnes = list(set(colonnes + self.hidden_columns))

        color = None
        if self.color in colonnes:
            color = self.color
        geometry = None
        if self.geometry in colonnes:
            geometry = self.geometry
        
        sub_df = self.df.loc[lignes, colonnes]
        
        return SfGeoDataFrame(df = sub_df, hidden_columns= self.hidden_columns, geometry= geometry, color= color)

    def rajouter_couleur(self, column_from: str, d: dict, color_column_name: str = 'couleur'):
        """
        Create a column 'color_column_name' to self.df, giving the color for each row of self.df. Update value of self.color to color_column_name.
        :param column_from: the column we use to choose the colors.
        :param d: a dictionnary where keys are values of self.df[column_from] and values are the corresponding colors.
        :param color_column_name: the name of the new column with colors.
        """
        if column_from not in self.df:
            raise MissingColumn(column_from)
        
        values = self.df[column_from].unique()
        for x in values:
            if not isinstance(x, str):
                raise TypeError(f"{x} must be a string")
            if not(x in d):
                raise KeyError(f"{x} is not in {d}")

        self.df[color_column_name] = [d[x] for x in self.df[column_from]]
        self.color = color_column_name
        print(f"La colonne '{color_column_name}' a bien été ajoutée au tableau")

    def coller(self, sdf: SfDataFrame):
        """
        Merges a SfDataFrame to self. It should have the same indexes. Attributes geometry, color are taken from self.
        :param sdf: the SfDataFrame we want to merge to our SfGeoDataFrame.
        """
        if len(self.df.index) != len(sdf.df.index):
            raise NotMatchIndexes()
        for i in self.df.index :
            if i not in sdf.df.index :
                raise NotMatchIndexes()
        
        df = self.df.merge(right = sdf.df, left_index=True, right_index= True)
        hidden_columns = list(set(sdf.hidden_columns + self.hidden_columns))
        return SfGeoDataFrame(df = df, hidden_columns= hidden_columns, geometry=self.geometry, color=self.color)
    
    def drop_hidden_columns(self):
        """
        Drops the hidden columns from self.df.
        :return: a SfGeoDataFrame without columns in self.hidden_columns.
        """
        new_df = self.df.drop(columns=self.hidden_columns)
        geometry = None
        if self.geometry not in self.hidden_columns :
            geometry = self.geometry
        return SfGeoDataFrame(df = new_df, geometry=geometry)

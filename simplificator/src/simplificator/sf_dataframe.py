import pandas as pd
import folium
from simplificator.sf_err import MissingColumn, MissingRow, SfSimplificatorUnknown, NotMatchIndexes


class SfDataFrame:
    def __init__(self, df: pd.DataFrame, hidden_columns: list[str] = []):
        """
        Creates a pandas DataFrame like; supposed to be easier to use.
        :param df: a pandas DataFrame, the data of the SfDataFrame.
        :param hidden_columns: names of the columns we don't want to show.
        """
        self.df = df
        for hidden_column in hidden_columns :
            if hidden_column not in self.df.columns:
                raise MissingColumn(hidden_column)
        self.hidden_columns = hidden_columns

    def afficher(self, n: int = 5) -> pd.DataFrame:
        """
        Gives the first n lines of the SfDataFrame.
        :param n: the number of lines we want to show.
        :return: a pd.DataFrame with n first rows of self.df.
        """
        if len(self.hidden_columns) == 0 :
            return self.df.head(n)
        df_temp = self.df.drop(columns = self.hidden_columns, axis = 1)
        return df_temp.head(n)

    def hide(self, column_name: str):
        """
        Add column 'column_name' to self.hidden_columns.
        :param column_name: the name of the column we want to hide.
        """
        if column_name not in self.df:
            raise MissingColumn(column_name)

        if column_name in self.hidden_columns:
            return
        self.hidden_columns.append(column_name)
    
    def show(self, column_name: str):
        """
        Remove column 'column_name' from self.hidden_columns.
        :param column_name: the name of the column we want to show.
        """
        if column_name not in self.df:
            raise MissingColumn(column_name)

        if column_name not in self.hidden_columns :
            return
        self.hidden_columns.remove(column_name)

    def afficher_le_nombre_de_lignes(self):
        """
        Prints the number of lines in self.df.
        """
        print(f"Il y a {self.df.shape[0]} lignes dans ce tableau.")

    def afficher_le_nombre_de_colonnes(self):
        """
        Prints the number of columns in self.df.
        """
        print(f"Il y a {self.df.shape[1]-len(self.hidden_columns)} colonnes dans ce tableau.")

    def afficher_le_nom_des_colonnes(self):
        """
        Prints the names of the columns in self.df.
        """
        result = "Les colonnes de ce tableau sont :"
        end = "."
        column_list = self.df.columns
        if len(column_list) > 20:
            column_list = column_list[:20]
            end = "..."
        for column_name in column_list :
            result += "\n" + column_name + ","
        print(result[:-1] + end)

    def afficher_les_valeurs_de_la_colonne(self, column_name: str, show_all: bool = False):
        """
        Prints the values of the column 'column_name'. If not 'show_all', max 20 values are printed.
        :param column_name: the name of the column
        :param show_all: boolean to override the limitation : max 20 values printed.
        """
        if column_name not in self.df:
            raise MissingColumn(column_name)

        values = self.df[column_name].unique()
        if show_all :
            print(values)
            return
        end = "."
        if len(values) > 20:
            values = values[:20]
            end = "\n .... IL Y A PLUS DE 2O VALEURS"
        result = f"Les valeurs de la colonne {column_name} sont :"
        for x in values:
            result += "\n-" + str(x) + ","
        print(result[:-1] + end)
    
    def avoir_la_colonne(self, column_name: str) -> pd.Series:
        """
        Gives the column of self.df with name 'column_name'.
        :param column_name: the name of the column in self.df we want to get.
        :return: a pd.Series, the column of self.df with name 'column_name'.
        """
        if column_name not in self.df:
            raise MissingColumn(column_name)

        return self.df[column_name]

    def avoir_element(self, row_index: int | str,  column_name: str) -> object:
        """
        Gives a specific element of self.df, on row : row_index and on colum : column_name.
        :param row_index: the index of the row of the element you want to get, in self.df.
        :param column_name: the name of the column of the element you want to get, in self.df.
        :return: the element on row : row_index and on colum : column_name.
        """
        if column_name not in self.df:
            raise MissingColumn(column_name)

        if row_index not in self.df.index:
            raise MissingRow(row_index)
            
        return self.df[column_name][row_index]

    def change_column(self, column_name: str, d: dict):
        """
        Changes all values of column 'column_name' according to dictionnary 'd'. Elements of self.df[column_name] must be strings.
        :param column_name: the name of the column in self.df we want to change.
        :param d: the dictionnary between the old values and the new ones.
        """
        if column_name not in self.df:
            raise MissingColumn(column_name)
        
        values = self.df[column_name].unique()
        for x in values:
            if not isinstance(x, str):
                raise TypeError(f"{x} must be a string")
            if not(x in d):
                raise KeyError(f"{x} is not in {d}")
            
        self.df[column_name] = [d[x] if x in d else None for x in self.df[column_name]]

    def sous_tableau(self, lignes: list = [], colonnes: list[str] = []):
        """
        Gives a subset of self.df, with rows in lignes an columns in columns.
        :param lignes: the index of the rows we want to put in our subset.
        :param columns: the column's name we want to keep in our subset.
        :return: a SfDataFrame, subset of self.df.
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
        
        sub_df = self.df.loc[lignes, colonnes]
        return SfDataFrame(df = sub_df, hidden_columns= self.hidden_columns)

    def copy(self):
        """
        Give a copy of the SfDataFrame.
        :return: a SfDataFrame which is a copy of self.
        """
        return self.sous_tableau()

    def get_dict_values_to_number(self) -> dict:
        """
        For each column, creates a dictionnary between values and number between 0 and n (n is the number of different values)
        :return: (dict, list) -dict where keys are columns of self.df, and values are the dictionnaries.
                              -list where values are the number of different in each column.
        """
        dict_values_to_number = {}
        min_categories = {}
        for column_name in self.df.columns :
            if column_name not in self.hidden_columns :
                d, n = self.get_column_dict_values_to_number(column_name=column_name)
                dict_values_to_number[column_name] = d
                min_categories[column_name] = n
        return dict_values_to_number, list(min_categories.values())

    def get_column_dict_values_to_number(self, column_name: str):
        """
        For one column, creates a dictionnary between values and number between 0 and n (n is the number of different values).
        The (n+1)th value always correspond to 'simplificator_unknown'.
        :param column_name: the name of the column we want to get a dictionnary.
        :return: (d, n): -d is the dictionnary between values of column column_name and number between 0 and n.
                          -n is the number of different values in this column.
        """
        if column_name not in self.df:
            raise MissingColumn(column_name)

        values = self.df[column_name].unique()
        values = [str(value) for value in values]
        if 'simplificator_unknown' in values :
            raise SfSimplificatorUnknown(column_name)
        else : 
            values.append('simplificator_unknown')
        n = len(values)
        d = {x : i for i, x in enumerate(values)}
        return d, n
    
    def coller(self, sdf):
        """
        Merges a SfDataFrame to self. It must have the same indexes.
        :param sdf: the SfDataFrame we want to merge to our SfDataFrame.
        """
        if len(self.df.index) != len(sdf.df.index):
            raise NotMatchIndexes()
        for i in self.df.index :
            if i not in sdf.df.index :
                raise NotMatchIndexes()
        
        df = self.df.merge(right = sdf.df, left_index=True, right_index= True)
        hidden_columns = list(set(sdf.hidden_columns + self.hidden_columns))
        return SfDataFrame(df = df, hidden_columns= hidden_columns)

    def drop_hidden_columns(self):
        """
        Drops the hidden columns from self.df.
        :return: a SfGeoDataFrame without columns in self.hidden_columns.
        """
        new_df = self.df.drop(columns=self.hidden_columns)
        return SfDataFrame(df = new_df)

import pandas as pd
import datetime
import numpy as np
from sklearn.naive_bayes import CategoricalNB
from simplificator.sf_dataframe import SfDataFrame
from simplificator.sf_err import MissingColumnTraining, NotTrained

class SfNaiveBayes:
    def __init__(self):
        """
        A copy of CategoricalNB from sklearn, supposed to be easier to use.
        """
        self.model = CategoricalNB()
        self.target = None #name of the column of the target
        self.dict_values_to_number = {} #dictionnary between values of each column and numbers between 0 and n, where n is the number of different values in the column. The value 'n' is always 'simplificator_unknown', to deal with unknown values.
        self.class_values = {}
        self.features = {}
        self.is_trained = False
        self.sample_train_number = 1
        self.class_count = []
    
    def entrainer(self, entree: SfDataFrame, sortie: SfDataFrame):
        """
        Fits self.model to predict 'sortie' with 'entree'.
        :param entree: a SfDataFrame with data corresponding to X_train.
        :param sortie: a SfDataFrame with data corresponding to y_train.
        """
        self.dict_values_to_number, self.model.min_categories = entree.get_dict_values_to_number()
        self.features = {key: i for i, key in enumerate(self.dict_values_to_number.keys())}
        entree = entree.drop_hidden_columns()
        sortie = sortie.drop_hidden_columns()
        X_train = self.translate(entree).df
        self.sample_train_number = sortie.df.shape[0]
        self.target = sortie.df.columns[0]
        self.model.fit(X_train, sortie.df[self.target])
        self.class_values = {key: i for i, key in enumerate(self.model.classes_)}
        self.class_count = [len(np.where(sortie.df[self.target].values == key)[0]) for key in self.model.classes_]
        self.is_trained = True
        print(f"L'IA a bien été entraînée sur les colonnes {list(self.features.keys())} à prédire la valeur de la colonne '{self.target}'.")

    def translate(self, data: SfDataFrame) -> SfDataFrame:
        """
        Translates, for each column, data to numbers between 0 and n, where n is the number of different values in the column.
        The (n+1)th values correspond to unknown values that the user would want to translate.
        :param data: a SfDataFrame to translate.
        :return: a SfDataFrame with numbers instead of values. 
        """
        new_data = data.copy()
        for column_name in new_data.df.columns :
            if column_name not in new_data.hidden_columns and column_name in self.dict_values_to_number:
                d = self.dict_values_to_number[column_name]
                new_data.df[column_name] = [d[str(x)] if str(x) in d else d['simplificator_unknown'] for x in new_data.df[column_name]]
        return new_data

    def predire(self, data: SfDataFrame) -> SfDataFrame:
        """
        Predicts values for the class, with new entries.
        :param data: a SfDataFrame with entries data. It must have columns included in those of the training dataframe. Order doesn't matter.
        :return: a SfDataFrame with one column named self.target.
        """
        func_name = "predire"
        if not self.is_trained :
            raise NotTrained(func_name)
        data = data.drop_hidden_columns()
        for column_name in data.df.columns:
            if column_name not in self.dict_values_to_number:
                raise MissingColumnTraining(column_name)
    
        data.df = data.df.reindex(columns=self.dict_values_to_number.keys())
        data_translated = self.translate(data)

        prediction = self._predict(data_translated.df)
        return SfDataFrame(df = prediction)
    
    def _predict(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Predicts a translated DataFrame (i.e. with numbers instead of values for features) according to self.model and Naive Bayes hypothesis.
        :param data: a pandas DataFrame with numbered data.
        :return: a pandas DataFrame with predictions.
        """
        result = ['' for i in range(len(data.index))]
        for i, index in enumerate(data.index):
            result[i] =  list(self.class_values.keys())[self._predict_vector(data.loc[index])]
        return pd.DataFrame(result, index = data.index, columns=[self.target])
    
    def _predict_vector(self, x: pd.Series):
        """
        Gives the class number whose probabilty  knowing X = x is the higher.
        :param x: a vector of features.
        :return: the index of the class whose probabilty is the higher knowing X = x.
        """
        P = np.array([self._proba(j, x) for j in range(len(self.class_values))]) #P[j] is the probability that y=self.class_list[j] knowing x = data
        p = np.max(P)
        return np.random.choice(np.where(P == p)[0])

    def _proba(self, j, x:pd.Series):
        """
        Estimates the probability that y = j and X = x, according to the 'naive' bayes hypothesis (conditional independance). The estimation is the product for all features i in x of : (number_of_occurence(x_i, j) + 1)/(number_of_occurence(j) + number of classes_values), times number_of_occurence(j).
        :param j: value of class y.
        :param x: a vector of features.
        :return: the estimation of the probability P(X = x, y = j) = P(X = x | y = j)*P(y = j).
        """
        prob = 1
        for column_name in x.index:
            k = self.features[column_name]
            count = self.model.category_count_[k][j]
            prob *= (count[x[column_name]]+ 1)/(self.class_count[j] + self.model.min_categories[k])
        prob *= self.class_count[j]/self.sample_train_number
        return prob

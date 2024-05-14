class MissingColumn(Exception):
    def __init__(self, column_name: str):
        super().__init__(f"Il n'y a pas de colonne '{column_name}' dans ce tableau.")

class MissingRow(Exception):
    def __init__(self, row_index: str):
        super().__init__(f"Il n'y a pas de ligne'{row_index}' dans ce tableau.")

class SfSimplificatorUnknown(Exception):
    def __init__(self, column_name: str):
        super().__init__(f"In column {column_name}, there should not be a value 'simplificator_unknown' in dataframe, it may creates issues.")

class NotMatchIndexes(Exception):
    def __init__(self):
        super().__init__(f"Indexes of the SfDataFrames must be the same.")

class MissingColumnTraining(Exception):
    def __init__(self, column_name):
        super().__init__(f"No column {column_name} was given during training.")

class NoJsonGeometry(Exception):
    def __init__(self, element):
        super().__init__(f"Element : {element} in geometry columns is not json.")

class NotTrained(Exception):
    def __init__(self, func_name):
        super().__init__(f"Erreur pendant l'execution de la méthode '{func_name}', le modèle n'a pas été entraîné. Utiliser la méthode 'entrainer' pour l'entraîner.")
## Simplificator

Simplificator is a package whose aim is to simplify the utilisation of pandas DataFrame, folium Map and Naïve Bayes classifier CategoricalNB from sklearn.
It is originally intended for secondary school students, so that they can have an introduction to data science and machine learning, without the difficulties of learning how to use pandas and the others libraries. Nevertheless, the package was made so that students could understand the keys ideas of handling datasets and training a ML model. 

See an example of an exercise about traffic in the city of Rennes here : __???__.

See `README.ipynb` for basic utilisation of __simplificator__.

Simplificator has 3 main classes : 
1. SfDataFrame
2. SfGeoDataFrame
3. SfNaiveBayes

SfDataFrame is a wrapper of pandas DataFrame, SfGeoDataFrame is a SfDataFrame with a column 'geometry' (as in a geopandas GeoDataFrame) with geometric information.
SfNaiveBayes is a sklearn CategoricalNB wrapper.
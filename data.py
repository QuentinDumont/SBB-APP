# -*- coding: utf-8 -*-
"""
Created on Thu Oct 11 10:53:11 2018
@author: Quentin
"""

import pandas as pd #Data Wrangling and Manipulation
import geopandas as gpd #To transform the SHP file with Geometry coordinates into DataFrames
from bokeh.models import ColumnDataSource, GeoJSONDataSource


""" Read fichier Data_Passengers & Cleaning"""

#Import passagierfrequenz.csv
data_passengers = pd.read_csv('passagierfrequenz.csv', sep=';',
                              engine='python', encoding = 'utf-8',
                              parse_dates=['Bezugsjahr'])

#Reading the TimeSeries Data
"""Unfortunately, after having a look into the data, there was only two dates availables ((1/1/2014) & (1/1/16)).
Therefore I worked with it as string in order to manipulate more easily and makes two columns out of it."""

#Keeping only the Year, removing Month and Days
data_passengers['Year'] = data_passengers['Bezugsjahr'].astype(str).str[0:4].astype(float)

#Removing non-informative information and droping NAN into Geopos, because Bokeh does not plot with NAN information
data_passengers = data_passengers.set_index('Bezugsjahr').drop(['Bemerkung', 'lod'], axis= 1).dropna(subset = ['geopos'])
#Filling with 0 - NAN information about passengers.
data_passengers[['DTV', 'DMW']] = data_passengers[['DTV', 'DMW']].fillna(0)

#data_passengers_chart, we take off geopos to make the file lighter
data_passengers_chart = data_passengers.drop(['geopos'], axis= 1)

#Sort values by Stations Names - To make the merge of Data_Passengers 2016 & Data_Passengers 2014 with no mistakes. Indexes match.
data_passengers_2016 = data_passengers_chart[data_passengers_chart['Year'] == 2016 ].sort_values('Bahnhof_Haltestelle')
data_passengers_2014 = data_passengers_chart[data_passengers_chart['Year'] == 2014 ].sort_values('Bahnhof_Haltestelle')

data_passengers_2016 = data_passengers_2016.reset_index()
data_passengers_on_change = data_passengers_2016.drop('Bezugsjahr', axis= 1)
data_passengers_on_change['DTV_2016'] = data_passengers_on_change['DTV']
data_passengers_on_change['DMW_2016'] = data_passengers_on_change['DMW']

data_passengers_2014 = data_passengers_2014.reset_index()
data_passengers_on_change['Year_2014'] = data_passengers_2014['Year']
data_passengers_on_change['DTV_2014'] = data_passengers_2014['DTV']
data_passengers_on_change['DMW_2014'] = data_passengers_2014['DMW']

"""Remove the now useless columns"""
data_passengers_on_change = data_passengers_on_change.drop(['DTV', 'DMW'], axis = 1)

#We create the ColumnDataSource for HBar Figure - DTW & DMW for 2014 + 2016
source_pass = ColumnDataSource(data_passengers_on_change)







"""MAP - Part 1 : Importation des données géographique /Data Geolocalisation"""

#Lecture du fichier Shapefile en DataFrame via GeoPandas pour Dessiner la Carte Suisse
cwd = os.getcwd()
temp_cwd = cwd + '\\geo_data\\'
gdf0 = gpd.read_file(temp_cwd + 'gadm36_CHE_0.shp')
gdf1 = gpd.read_file(temp_cwd + 'gadm36_CHE_1.shp')
gdf1_crs = gdf1.to_crs({'init': 'epsg:3857'})

#Lecture fichier Shapefile en DataFrame via GeoPandas Pour les differentes Stations
gdf_loc_station = gpd.read_file('lorastation.shp', encoding = 'utf-8')
gdf_loc_station = gdf_loc_station.drop(20).reset_index(drop= True)
gdf_loc_station_crs = gdf_loc_station.to_crs({'init': 'epsg:3857'})

# Lecture fichier SHP de l'ensemble des lignes - Géolocalisation
gdf_loc_line = gpd.read_file('linie-mit-betriebspunkten.shp', encoding = 'utf-8')
gdf_loc_line = gdf_loc_line.sort_values(['linie', 'km']) #Tri pour dessiner les arrêts les uns après les autres.
gdf_loc_line_crs = gdf_loc_line.to_crs({'init': 'epsg:3857'}) #Conversion au format CRS 3857

#3er Onglet - Onglet de la carte suisse avec les Lignes de Trains.
#Conversion des frontières
gdf0_crs = gdf0.to_crs({'init': 'epsg:3857'})
gdf_loc_line_crs = gdf_loc_line.to_crs({'init': 'epsg:3857'})

""" MAP - Part 2 : Création du DF juste pour les lignes de la suisse"""

gdf_loc_line = gdf_loc_line.drop(['lod', 'what3word_e','what3word_i', 'what3word_f', 'what3word_d'], axis = 1)

def getPointCoords(row, geom, coord_type):
    """Calculates coordinates ('x' or 'y') of a Point geometry"""
    if coord_type == 'x':
        return row[geom].x
    elif coord_type == 'y':
        return row[geom].y


list_df = []
list_x_coord = []
list_y_coord = []

list_lines = gdf_loc_line.linie.unique().tolist()


# Calculate x coordinates pour éviter les connections entre deux lignes différentes
gdf_loc_line_crs['x'] = gdf_loc_line_crs.apply(getPointCoords, geom='geometry', coord_type='x', axis=1)
# Calculate y coordinates pour éviter les connections entre deux lifgnes différents
gdf_loc_line_crs['y'] = gdf_loc_line_crs.apply(getPointCoords, geom='geometry', coord_type='y', axis=1)

for i, linie in enumerate(list_lines) :
    df_line = gdf_loc_line_crs[gdf_loc_line_crs['linie'] == linie]
    a = df_line.x.tolist()
    list_x_coord.append(a)
    b = df_line.y.tolist()
    list_y_coord.append(b)

gdf_map_crs = gdf_loc_line_crs[['linie', 'linienname']].drop_duplicates().reset_index(drop = True)
serie_x_coord = pd.Series(list_x_coord)
serie_y_coord = pd.Series(list_y_coord)
gdf_map_crs['x_coord'] = serie_x_coord
gdf_map_crs['y_coord'] = serie_y_coord
source_map_crs = ColumnDataSource(gdf_map_crs)

list_lines = gdf_loc_line.linie.unique().tolist()
list_namelines = gdf_loc_line.linienname.unique().tolist()
gdf0_crs = gdf0.to_crs({'init': 'epsg:3857'})
source_geo_crs = GeoJSONDataSource(geojson=gdf0_crs.to_json())
source_geo_station = GeoJSONDataSource(geojson=gdf_loc_station.to_json())
source_geo_station_crs = GeoJSONDataSource(geojson=gdf_loc_station_crs.to_json())
source_geo_line = GeoJSONDataSource(geojson=gdf_loc_line.to_json())
source_geo_line_crs = GeoJSONDataSource(geojson=gdf_loc_line_crs.to_json())




""" Data Top 10-20-30-50-100 """
top_AZ = data_passengers_on_change.sort_values('Bahnhof_Haltestelle')
top_2016 = data_passengers_on_change.drop(['Year_2014', 'DTV_2014', 'DMW_2014'], axis = 1)
top_2014 = data_passengers_on_change.drop(['Year', 'DTV_2016', 'DMW_2016'], axis = 1)

top_10_DMW16 = data_passengers_on_change.sort_values('DMW_2016', ascending = False).iloc[0:10]
top_10_DMW16_rev = data_passengers_on_change.sort_values('DMW_2016', ascending = True).iloc[0:10]

top_20_DMW16 = data_passengers_on_change.sort_values('DMW_2016', ascending = False).iloc[0:20]
top_20_DMW16_rev = data_passengers_on_change.sort_values('DMW_2016', ascending = True).iloc[0:20]

top_50_DMW16 = data_passengers_on_change.sort_values('DMW_2016', ascending = False).iloc[0:50]

top_100_DMW16 = data_passengers_on_change.sort_values('DMW_2016', ascending = False).iloc[0:10]

top_500_DMW16 = data_passengers_on_change.sort_values('DMW_2016', ascending = False).iloc[0:500]


top_10_DMW14 = data_passengers_on_change.sort_values('DMW_2014', ascending = False).iloc[0:10]

top_20_DMW14 = data_passengers_on_change.sort_values('DMW_2014', ascending = False).iloc[0:20]

top_50_DMW14 = data_passengers_on_change.sort_values('DMW_2014', ascending = False).iloc[0:50]

top_100_DMW14 = data_passengers_on_change.sort_values('DMW_2014', ascending = False).iloc[0:10]

top_500_DMW14 = data_passengers_on_change.sort_values('DMW_2014', ascending = False).iloc[0:500]

data_40000 =  data_passengers_on_change[data_passengers_on_change['DTV_2016'] < 40000]

# -*- coding: utf-8 -*-
"""
Created on Thu Oct 11 11:11:40 2018

@author: Quentin
"""
import os
from bokeh.io import curdoc
from bokeh.models import Tabs, Panel
from bokeh.models.widgets import TableColumn, DataTable

#load data.py
from data import *

from bokeh.layouts import row, column


#Table Lines Localisation
gdf_loc_line_table = gdf_loc_line.drop('geometry', axis= 1)
source_table = ColumnDataSource(gdf_loc_line_table.sort_values(['bezeichnung']))

columns = [
        TableColumn(field = 'bezeichnung', title = 'Stopname', width = 140),
        TableColumn(field = 'linie', title = 'Lines n°', width = 80),
        TableColumn(field = 'linienname', title = 'Line Name', width = 200),
        TableColumn(field = 'km', title = 'Number of Km from Starting point', width = 100)
    ]

data_table_loc = DataTable(source=source_table, columns=columns, height = 500, width = 1000)



#Table Passengers
source_table_passengers = ColumnDataSource(data_passengers)

from bokeh.models.widgets.tables import DateFormatter

columns_passengers = [
    TableColumn(field = 'Bezugsjahr', title = 'Date', formatter = DateFormatter(format = "%Y")),
    TableColumn(field = 'Code', title = 'Code'),
    TableColumn(field = 'Bahnhof_Haltestelle', title = 'Stop'),
    TableColumn(field = 'DTV', title = 'DTV'),
    TableColumn(field = 'DMW', title = 'DMW'),
    TableColumn(field = 'Eigner', title = 'Eigner'),
    TableColumn(field = 'geopos', title = 'GeoPos'),
                     ]

data_table_passengers = DataTable(source = source_table_passengers, columns = columns_passengers, height = 500, width = 1000)


#Create the layout, column
layout_table = column(data_table_loc, data_table_passengers)

onglet_1 = Panel(child = layout_table, title="Data")
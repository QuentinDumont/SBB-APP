# -*- coding: utf-8 -*-
"""
Created on Thu Oct 11 11:39:53 2018

@author: Quentin
"""

import os
from bokeh.io import curdoc
from bokeh.models import HoverTool, Select
from bokeh.models.widgets import TableColumn, DataTable
from bokeh.plotting import figure
from bokeh.transform import dodge
from bokeh.core.properties import value
import random
from bokeh.layouts import widgetbox
from bokeh.models.widgets import CheckboxGroup

from bokeh.tile_providers import CARTODBPOSITRON

#load data.py
from data import *

from bokeh.layouts import row, column


temp_f= figure(width = 1500, height = 1500, 
               title = 'Public Train Network Switzerland (SBB/CFF)',
			   x_axis_type="mercator", y_axis_type="mercator")

temp_f.title.text_color = "black"
temp_f.title.text_font_style = "bold"

#Lecute du fichier Shapefile pour dessiner les contours du Pays.
temp_p1 = temp_f.patches('xs','ys', source = source_geo_crs, line_color = 'blue', alpha = 0.1, fill_color = 'white', fill_alpha = 0.0001)
"""temp_f.add_tools(HoverTool(renderers = [temp_p1], tooltips=[('Canton', '@NAME_1')]))""" # Fonctionne Sur GDF1 et non GDF0 


#p_3 circle of every single stations
temp_p3 = temp_f.circle('x','y', source = source_geo_line_crs, 
                        color = 'gray' , fill_color = 'white', 
                        size = 5, legend ='Stations')
temp_f.add_tools(HoverTool(renderers = [temp_p3], tooltips = [('Stop Name', '@bezeichnung')]))

#p_4 line of every trainline
temp_p4 = temp_f.multi_line(xs = 'x_coord' , ys = 'y_coord', line_width=1, line_color ='red', source = source_map_crs)
temp_f.add_tools(HoverTool(renderers = [temp_p4], tooltips = [('Line', '@linie'),
                           ('Name Line', '@linienname')]))

#Drawings of the Main Station - To make more accurate
source_geo_station_crs = GeoJSONDataSource(geojson=gdf_loc_station_crs.to_json())
temp_p2 = temp_f.circle('x','y', source = source_geo_station_crs, 
                        color = 'black',  size = 10,
                        alpha =0.60, legend = 'Main Station')
    
temp_f.xgrid.grid_line_color = None
temp_f.ygrid.grid_line_color = None 

temp_f.xaxis.major_tick_line_color = None  # turn off x-axis major ticks
temp_f.xaxis.minor_tick_line_color = None  # turn off x-axis minor ticks
temp_f.yaxis.major_tick_line_color = None  # turn off y-axis major ticks
temp_f.yaxis.minor_tick_line_color = None  # turn off y-axis minor ticks
temp_f.xaxis.major_label_text_color = None  #note that this leaves space between the axis and the axis label  
temp_f.yaxis.major_label_text_color = None  #note that this leaves space between the axis and the axis label  

temp_f.outline_line_color = 'black'
temp_f.legend.location ='top_left'

#Creation of the list for the callback version (Optimisation possible)

connections = []
list_namelines = gdf_loc_line.linienname.unique().tolist()

for cities in list_namelines : 
    city = str(cities).split(' - ')
    connection = (city [0] +' -> ' + city[-1])
    connections.append(connection)

list_dd_menu = []
list_dd_menu.append(('All Lines', 'all'))

for i, line in enumerate(list_lines) : 
    l = str(line).split('.')[0]
    a = (l + ' - ' + connections[i],str(line))
    list_dd_menu.append(a)

list_dd_menu_inv = []
for i, line in enumerate(list_dd_menu) :
    inv = (line[1], line[0])
    list_dd_menu_inv.append(inv)

list_dd_menu_inv_str = []
for i, e in enumerate(list_dd_menu_inv) :
    list_dd_menu_inv_str.append(e[1])

list_lines_str = ['All Lines']
for elt in list_lines :
    elt_str = str(elt)
    list_lines_str.append(elt_str)
    
select_line = Select(title = 'Choose a Line', value = 'All Lines', options = list_dd_menu_inv_str)


def callback_dd(attr, old, new) :
        for i in range (1, len(list_dd_menu_inv_str)) :
            if select_line.value == 'All Lines' : 
                source_map_crs.data = ColumnDataSource(gdf_map_crs).data
            elif select_line.value == list_dd_menu_inv_str[i] : 
                source_map_crs.data = ColumnDataSource(gdf_map_crs[gdf_map_crs['linie'].astype(str) == str(list_lines_str[i])]).data
                
select_line.on_change('value', callback_dd)

#Nouveau CallBackn box_group

checkbox_group = CheckboxGroup(
        labels=['Mains Stations', 'Stations', 'Lines'], active=[0, 1, 2])

def callback_check(attr, old, new) :
            if checkbox_group.active == [0] :
                temp_p2.visible = True
                temp_p3.visible = False
                temp_p4.visible = False
            elif checkbox_group.active == [0,1] : 
                temp_p2.visible = True
                temp_p3.visible = True
                temp_p4.visible = False
            elif checkbox_group.active == [0,2] : 
                temp_p2.visible = True
                temp_p3.visible = False
                temp_p4.visible = True
            elif checkbox_group.active == [0,1,2] : 
                temp_p2.visible = True
                temp_p3.visible = True
                temp_p4.visible = True

checkbox_group.on_click(callback_check)


temp_f.add_tile(CARTODBPOSITRON)

layout_map = column(select_line, widgetbox(checkbox_group),temp_f)   

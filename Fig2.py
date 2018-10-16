# -*- coding: utf-8 -*-
"""
Created on Thu Oct 11 11:24:28 2018

@author: Quentin
"""

import os
from bokeh.io import curdoc
from bokeh.models import HoverTool, Select, Span, LabelSet, Label
from bokeh.models.widgets import TableColumn, DataTable, Slider
from bokeh.plotting import figure
from bokeh.transform import dodge
from bokeh.core.properties import value
from bokeh.layouts import widgetbox



#load data.py
from data import *

from bokeh.layouts import row, column

source_pass = ColumnDataSource(data_passengers_on_change)

# Create a new plot: plot
fig_hbar = figure(x_range = (0, max(data_passengers_on_change['DMW_2016']) + 50000),
           y_range = data_passengers_on_change['Bahnhof_Haltestelle'].sort_values(ascending = False),
           plot_height = 10000, plot_width=1000,
           title = 'Passenger per Station')

# Add a line to the plot
p_hbar1 = fig_hbar.hbar(y=dodge('Bahnhof_Haltestelle', +0.30, range = fig_hbar.y_range) , right = 'DTV_2014',
              source = source_pass,  
              height = 0.20,
              color="#718dbf", legend=value("DTV 2014"))

p_hbar3 = fig_hbar.hbar(y=dodge('Bahnhof_Haltestelle', +0.10, range = fig_hbar.y_range) , right = 'DMW_2014',
              source = source_pass,  
              height = 0.20,
              color="lightblue", legend=value("DMW 2014"))

p_hbar2 = fig_hbar.hbar(y=dodge('Bahnhof_Haltestelle', -0.10, range = fig_hbar.y_range) , right = 'DTV_2016',
              source = source_pass,  
              height = 0.20,
              color="#e84d60", legend=value("DTV 2016"))

p_hbar4 = fig_hbar.hbar(y=dodge('Bahnhof_Haltestelle', -0.30, range = fig_hbar.y_range) , right = 'DMW_2016',
              source = source_pass,  
              height = 0.20,
              color="pink", legend=value("DMW 2016"))




#Add HoverTool
fig_hbar.add_tools(HoverTool(mode='hline', renderers = [p_hbar1], tooltips = [('DTV_2014', '@DTV_2014'),
                                                   ('Station', '@Bahnhof_Haltestelle')]))

fig_hbar.add_tools(HoverTool(mode='hline', renderers = [p_hbar3], tooltips = [('DMW_2014', '@DMW_2014'),
                                                   ('Station', '@Bahnhof_Haltestelle')]))

fig_hbar.add_tools(HoverTool(mode='hline', renderers = [p_hbar2], tooltips = [('DTV_2016', '@DTV_2016'),
                                                   ('Station', '@Bahnhof_Haltestelle')]))

fig_hbar.add_tools(HoverTool(mode='hline', renderers = [p_hbar4], tooltips = [('DMV_2016', '@DMW_2016'),
                                                   ('Station', '@Bahnhof_Haltestelle')]))
#Add Span
p_hbar5 = Span(location=10000,
               dimension='height', line_color='green',
               line_dash='dashed', line_width=2)

fig_hbar.add_layout(p_hbar5)


#Add Slider to Span (fig_hbar5)
slider = Slider(start=0, end=500000, value=p_hbar5.location, step=5000, title="Span Bar")

def callback_span(attr, new, old) :
    p_hbar5.location = slider.value
slider.on_change('value', callback_span)

#Remove inconvenient formatter / Layout
fig_hbar.xaxis[0].formatter.use_scientific = False
fig_hbar.ygrid.grid_line_color = None
fig_hbar.legend.location = "top_right"
fig_hbar.legend.orientation = "horizontal"
fig_hbar.xaxis.axis_label = 'Number of Passengers'
fig_hbar.yaxis.axis_label = 'City Name'


#Add Callback
menu = Select(options=['Toutes', 'Top 10', 'Top 20', '<= 40000 Passengers'], value='Toutes', title='Nombres de Villes')



def callback(attr, old, new):
    if menu.value == 'Toutes' : 
        source_pass.data = ColumnDataSource(data_passengers_on_change).data
        fig_hbar.height = 10000
        fig_hbar.width = 3000
        fig_hbar.x_range.start = 0
        fig_hbar.x_range.end = (max(data_passengers_on_change['DMW_2016']) + 50000)
        fig_hbar.y_range.factors = data_passengers_on_change['Bahnhof_Haltestelle'].sort_values(ascending = False).tolist()
        
    elif menu.value == 'Top 10':
        source_pass.data = ColumnDataSource(top_10_DMW16).data
        fig_hbar.y_range.factors = top_10_DMW16['Bahnhof_Haltestelle'].sort_values(ascending = False).tolist()
        fig_hbar.x_range.start = 0
        fig_hbar.x_range.end = (max(data_passengers_on_change['DMW_2016']) + 50000)
        fig_hbar.height = 800
        fig_hbar.width = 1000
        
    elif menu.value == 'Top 20' : 
        source_pass.data = ColumnDataSource(top_20_DMW16).data
        fig_hbar.y_range.factors = top_20_DMW16['Bahnhof_Haltestelle'].sort_values(ascending = False).tolist()
        fig_hbar.height = 800
        fig_hbar.width = 1000
        fig_hbar.x_range.start = 0
        fig_hbar.x_range.end = (max(data_passengers_on_change['DMW_2016']) + 50000)
        
    elif menu.value == '<= 40000 Passengers' :
        source_pass.data = ColumnDataSource(data_40000).data
        fig_hbar.y_range.factors = data_40000['Bahnhof_Haltestelle'].sort_values(ascending = False).tolist()
        fig_hbar.height = 9000
        fig_hbar.width = 2000
        fig_hbar.x_range.start = 0
        fig_hbar.x_range.end = (max(data_40000['DMW_2016']) + 2000)
        

menu.on_change('value', callback)

  # 2nd Menu 
menu_order = Select(options=['A => Z', 'Z => A'], value = 'A => Z', title = "Order")

def callback_order (attr, old, new) : 
    if menu_order.value =='A => Z' : 
        list_y_range = list(sorted(fig_hbar.y_range.factors, reverse = True))
        fig_hbar.y_range.factors = list_y_range
    elif menu_order.value == 'Z => A' :
        list_y_range = list(sorted(fig_hbar.y_range.factors))
        fig_hbar.y_range.factors = list_y_range       

    
    
menu_order.on_change('value', callback_order)

#3rd Menu

menu_year = Select(options=['2014', '2016', '2014/16'], value='2014/16', title='Year(s)')

def callback_year (attr, old, new) : 
    if menu_year.value == '2014/16' : 
        if menu_dtv.value == 'DTV + DMV' : 
            p_hbar1.visible = True
            p_hbar2.visible = True
            p_hbar3.visible = True
            p_hbar4.visible = True
        elif menu_dtv.value == 'DTV' :
            p_hbar1.visible = True
            p_hbar2.visible = True
            p_hbar3.visible = False
            p_hbar4.visible = False
        elif menu_dtv.value == 'DMW' :
            p_hbar1.visible = False
            p_hbar2.visible = False
            p_hbar3.visible = True
            p_hbar4.visible = True
            
    elif menu_year.value == '2014' :
        if menu_dtv.value == 'DTV + DMV' : 
            p_hbar1.visible = True
            p_hbar2.visible = False
            p_hbar3.visible = True
            p_hbar4.visible = False
        elif menu_dtv.value == 'DTV' :
            p_hbar1.visible = True
            p_hbar2.visible = False
            p_hbar3.visible = False
            p_hbar4.visible = False
        elif menu_dtv.value == 'DMW' :
            p_hbar1.visible = False
            p_hbar2.visible = False
            p_hbar3.visible = True
            p_hbar4.visible = False
            
    elif menu_year.value == '2016' :
        if menu_dtv.value == 'DTV + DMV' : 
            p_hbar1.visible = False
            p_hbar2.visible = True
            p_hbar3.visible = False
            p_hbar4.visible = True
        elif menu_dtv.value == 'DTV' :
            p_hbar1.visible = False
            p_hbar2.visible = True
            p_hbar3.visible = False
            p_hbar4.visible = False
        elif menu_dtv.value == 'DMW' :
            p_hbar1.visible = False
            p_hbar2.visible = False
            p_hbar3.visible = False
            p_hbar4.visible = True
        

menu_year.on_change('value', callback_year)


menu_dtv = Select(options=['DTV', 'DMW', 'DTV + DMV'], value='DTV + DMV', title='DTV or DMW')

def callback_dtv (attr, old, new) : 
    if menu_dtv.value == 'DTV + DMV' : 
        if menu_year.value == '2014/16' :
            p_hbar1.visible = True
            p_hbar3.visible = True
            p_hbar2.visible = True
            p_hbar4.visible = True
        elif menu_year.value == '2014' :
            p_hbar2.visible = False
            p_hbar4.visible = False
            p_hbar1.visible = True
            p_hbar3.visible = True
        elif menu_year.value == '2016' :
            p_hbar1.visible = False
            p_hbar3.visible = False
            p_hbar2.visible = True
            p_hbar4.visible = True
            
    elif menu_dtv.value == 'DTV' :
        if menu_year.value == '2014/16' :
            p_hbar1.visible = True
            p_hbar3.visible = False
            p_hbar2.visible = True
            p_hbar4.visible = False
        elif menu_year.value == '2014' :
            p_hbar2.visible = False
            p_hbar4.visible = False
            p_hbar1.visible = True
            p_hbar3.visible = False
        elif menu_year.value == '2016' :
            p_hbar1.visible = False
            p_hbar3.visible = False
            p_hbar2.visible = True
            p_hbar4.visible = False
            
    elif menu_dtv.value == 'DMW' :
        if menu_year.value == '2014/16' :
            p_hbar1.visible = False
            p_hbar3.visible = True
            p_hbar2.visible = False
            p_hbar4.visible = True
        elif menu_year.value == '2014' :
            p_hbar2.visible = False
            p_hbar4.visible = False
            p_hbar1.visible = False
            p_hbar3.visible = True
        elif menu_year.value == '2016' :
            p_hbar1.visible = False
            p_hbar3.visible = False
            p_hbar2.visible = False
            p_hbar4.visible = True
            
menu_dtv.on_change('value', callback_dtv)

#Add labels 
"""
labels = LabelSet(x='DTV_2014', y='Bahnhof_Haltestelle', text='DTV_2014', level='glyph', text_font_size='6pt',
              x_offset=5, y_offset=15, source=source_pass, render_mode='canvas')
labels2 = LabelSet(x='DTV_2016', y='Bahnhof_Haltestelle', text='DTV_2016', level='glyph', text_font_size='6pt',
              x_offset=5, y_offset=5, source=source_pass, render_mode='canvas')
labels3 = LabelSet(x='DMW_2014', y='Bahnhof_Haltestelle', text='DMW_2014', level='glyph', text_font_size='6pt',
              x_offset=5, y_offset=-5, source=source_pass, render_mode='canvas')
labels4 = LabelSet(x='DMW_2016', y='Bahnhof_Haltestelle', text='DMW_2016', level='glyph', text_font_size='6pt',
              x_offset=5, y_offset=-15, source=source_pass, render_mode='canvas')


fig_hbar.add_layout(labels)
fig_hbar.add_layout(labels2)
fig_hbar.add_layout(labels3)
fig_hbar.add_layout(labels4)
"""


# Arrange plots and widgets in layouts
row1 = row(menu, menu_order, menu_year, menu_dtv, slider)
layout_hbar = column(row1, fig_hbar)

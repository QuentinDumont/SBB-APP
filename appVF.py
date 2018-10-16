# -*- coding: utf-8 -*-
"""
Created on Thu Oct 11 11:05:03 2018

@author: Quentin
"""

import os
from bokeh.io import curdoc
from bokeh.models import Tabs

#load data.py
from data import *
from Fig1 import *
from Fig2 import *
from Fig3 import *


""" Compilation de nos trois Onglets / 
    onglet_1 : nos données
    onglet 2 : fig_hbar : Histogramme Horizontal
    Onglet 3 : La map de suisse"""

onglet_1 = Panel(child = layout_table, title="Data")
onglet_2 = Panel(child = layout_hbar, title = "Data Visualisation")
onglet_3 = Panel(child = layout_map, title = "Swiss Map")

tabs = Tabs(tabs=[onglet_1, onglet_2, onglet_3])

# Add the plot to the current document
curdoc().add_root(tabs)

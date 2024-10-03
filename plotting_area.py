#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct  3 14:18:33 2024

@author: aaditya
"""

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from xopt.generators.bayesian.visualize import visualize_generator_model

class PlottingArea:
    def __init__(self, parent=None):
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
    
    def update_plot(self, X, vocs, variable_names, reference_point, show_acquisition):
        self.figure.clear()
        fig, ax = visualize_generator_model(
            X.generator,
            variable_names=variable_names,
            reference_point=reference_point,
            show_acquisition=show_acquisition
        )
        self.canvas.figure = fig
        self.canvas.draw()
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct  3 14:18:33 2024

@author: aaditya
"""
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from PyQt5.QtWidgets import QVBoxLayout, QWidget
from xopt.generators.bayesian.visualize import visualize_generator_model

class PlottingArea(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Create a layout for the plot area without pre-filling it with a plot
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

    def update_plot(self, xopt_obj, variable_names, reference_point, show_acquisition, show_samples, show_prior_mean, show_feasibility, n_grid):
        # Clear the existing layout (remove previous plot if any)
        for i in reversed(range(self.layout.count())):
            widget_to_remove = self.layout.itemAt(i).widget()
            if widget_to_remove is not None:
                widget_to_remove.setParent(None)

        # Create a new figure and canvas
        figure = Figure()
        canvas = FigureCanvas(figure)

        # Generate the new plot using visualize_generator_model
        fig, ax = visualize_generator_model(
            xopt_obj.generator,
            variable_names=variable_names,
            reference_point=reference_point,
            show_acquisition=show_acquisition,
            show_samples=show_samples,
            show_prior_mean=show_prior_mean,
            show_feasibility=show_feasibility,
            n_grid=n_grid
        )

        # Adjust padding inside the figure
        fig.tight_layout(pad=2)  # Adds padding between plot elements

        # Set the new figure to the canvas and draw it
        canvas.figure = fig
        canvas.draw()

        # Add the new canvas to the layout
        self.layout.addWidget(canvas)

        # Ensure the layout is updated
        self.updateGeometry()

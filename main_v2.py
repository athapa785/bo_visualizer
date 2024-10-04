#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct  3 14:18:00 2024

@author: aaditya
"""

import sys
from PyQt5.QtWidgets import QApplication, QHBoxLayout, QWidget, QVBoxLayout, QSizePolicy
from model_visualization_example import X, vocs
from ui_components import UIComponents
from plotting_area import PlottingArea
from model_logic import ModelLogic

class PlotWidget(QWidget):
    def __init__(self, parent=None, xopt_obj=None):
        super().__init__(parent)

        self.model_logic = ModelLogic(xopt_obj if xopt_obj else X, vocs)
        self.ui_components = UIComponents(vocs)
        self.plotting_area = PlottingArea()

        main_layout = QHBoxLayout(self)

        controls_layout = QVBoxLayout()

        # Add controls
        controls_layout.addLayout(self.ui_components.create_axis_layout())
        controls_layout.addWidget(self.ui_components.create_reference_inputs())
        controls_layout.addWidget(self.ui_components.create_options_section())
        controls_layout.addLayout(self.ui_components.create_buttons())

        main_layout.addLayout(controls_layout)

        # Make sure the plotting area is expanding, set stretch to make it fill the space
        main_layout.addWidget(self.plotting_area.canvas, stretch=1)


        self.setLayout(main_layout)
        self.apply_style_sheet()

        # Connect update button to plot update function
        self.ui_components.update_button.clicked.connect(self.update_plot)

        # Ensure the canvas geometry is updated explicitly
        self.plotting_area.canvas.updateGeometry()

        

    def apply_style_sheet(self):
        # Load the style.qss file
        with open("style.qss", "r") as file:
            style_sheet = file.read()

        # Apply the loaded style sheet
        self.setStyleSheet(style_sheet)    

    def update_plot(self):
        variable_names = [self.ui_components.x_axis_combo.currentText(), self.ui_components.y_axis_combo.currentText()]
        variable_names = [var for var in variable_names if var != ""]

        reference_point = self.model_logic.get_reference_points(self.ui_components.ref_inputs, variable_names)
        self.plotting_area.update_plot(
            self.model_logic.X,
            vocs,
            variable_names,
            reference_point,
            self.ui_components.acq_func_checkbox.isChecked()
        )


if __name__ == "__main__":
    app = QApplication(sys.argv)
    xopt_instance = X  # You can pass a different Xopt object here if needed
    window = PlotWidget(xopt_obj=xopt_instance)
    window.setWindowTitle("BO Visualizer")
    window.resize(1000, 600)
    window.show()
    sys.exit(app.exec_())
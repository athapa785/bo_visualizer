#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct  3 14:18:00 2024

@author: aaditya
"""

import sys
from PyQt5.QtWidgets import QApplication, QHBoxLayout, QWidget, QVBoxLayout
from model_visualization_example import X, vocs
from ui_components import UIComponents
from plotting_area import PlottingArea
from model_logic import ModelLogic
from PyQt5.QtCore import Qt
import qtmodern.styles

class BOPlotWidget(QWidget):
    def __init__(self, parent=None, xopt_obj=None):
        super().__init__(parent)

        self.model_logic = ModelLogic(xopt_obj if xopt_obj else X, vocs)
        self.ui_components = UIComponents(xopt_obj.vocs if xopt_obj else vocs)
        self.plotting_area = PlottingArea()

        main_layout = QHBoxLayout(self)
        controls_layout = QVBoxLayout()

        # Add controls
        controls_layout.addLayout(self.ui_components.create_axis_layout())
        controls_layout.addWidget(self.ui_components.create_reference_inputs())
        controls_layout.addWidget(self.ui_components.create_options_section())
        controls_layout.addLayout(self.ui_components.create_buttons())

        main_layout.addLayout(controls_layout)

        # Add the entire PlottingArea widget and make sure it stretches
        main_layout.addWidget(self.plotting_area, stretch=1)

        self.setLayout(main_layout)
        self.apply_style_sheet()

        # Set default selections for X-axis and Y-axis dropdowns
        self.ui_components.x_axis_combo.setCurrentIndex(0)  # Default to x0 for X-axis
        self.ui_components.y_axis_combo.setCurrentIndex(1)  # Default to x1 for Y-axis

        # Connect update button to plot update function
        self.ui_components.update_button.clicked.connect(self.update_plot)

        # Connect dropdown selections to reference point updates
        self.ui_components.x_axis_combo.currentIndexChanged.connect(self.on_axis_selection_changed)
        self.ui_components.y_axis_combo.currentIndexChanged.connect(self.on_axis_selection_changed)

        self.setSizePolicy(self.sizePolicy().Expanding, self.sizePolicy().Expanding)

        # Trigger the axis selection changed to disable reference points for default selected variables
        self.on_axis_selection_changed()
        # Connect the Y-axis checkbox state change to the axis selection changed handler
        self.ui_components.y_axis_checkbox.stateChanged.connect(self.on_axis_selection_changed)

        self.resize(1000, 720)

    def on_axis_selection_changed(self):
        """Update reference points as soon as the dropdown selections change."""
        self.selected_variables = []

        # Always include X-axis variable
        x_var = self.ui_components.x_axis_combo.currentText()
        if x_var:
            self.selected_variables.append(x_var)

        # Include Y-axis variable only if the checkbox is checked
        if self.ui_components.y_axis_checkbox.isChecked():
            y_var = self.ui_components.y_axis_combo.currentText()
            if y_var:
                self.selected_variables.append(y_var)

        # Update the reference point table based on the selected variables
        self.update_reference_point_table(self.selected_variables)


    def apply_style_sheet(self):
        # Load and apply custom stylesheet
        with open("style.qss", "r") as file:
            custom_stylesheet = file.read()

        self.setStyleSheet(custom_stylesheet)

    def update_plot(self):
        # Get selected variables
        selected_variables = self.selected_variables

        # Disable and gray out the reference points for selected variables
        self.update_reference_point_table(selected_variables)

        # Get reference points for non-selected variables
        reference_point = self.model_logic.get_reference_points(self.ui_components.ref_inputs, selected_variables)


        #Resizing window to fit plots properly
        # Resizing window to fit plots properly
        acq_chk = self.ui_components.acq_func_checkbox.isChecked()
        prior_mean_chk = self.ui_components.show_prior_mean_checkbox.isChecked()
        feas_chk = self.ui_components.show_feasibility_checkbox.isChecked()

        if self.ui_components.y_axis_checkbox.isChecked() == True:

            # Set width based on prior_mean_chk
            width = 1400 if prior_mean_chk else 1000

            # Set height based on acq_chk and feas_chk
            if acq_chk and not prior_mean_chk and feas_chk:
                height = 820
            elif acq_chk or feas_chk:
                height = 780
            else:
                height = 720

        else:

            width = 1000

            # Set height based on acq_chk and feas_chk
            if acq_chk and feas_chk:
                height = 780
            else:
                height = 720

        self.resize(width, height)

        # Update the plot with the selected variables and reference points
        self.plotting_area.update_plot(
            self.model_logic.xopt_obj,
            selected_variables,
            reference_point,
            self.ui_components.acq_func_checkbox.isChecked(),
            self.ui_components.show_samples_checkbox.isChecked(),
            self.ui_components.show_prior_mean_checkbox.isChecked(),
            self.ui_components.show_feasibility_checkbox.isChecked(),
            self.ui_components.n_grid.value()
        )

    def update_reference_point_table(self, selected_variables):
        """ Disable and gray out reference points for selected variables """
        for i, var_name in enumerate(self.model_logic.vocs.variable_names):
            # Get the reference point item from the table
            ref_item = self.ui_components.ref_inputs[i]

            if var_name in selected_variables:
                # Disable editing and gray out the background
                ref_item.setFlags(ref_item.flags() & ~Qt.ItemIsEditable)
                ref_item.setBackground(Qt.lightGray)
                ref_item.setForeground(Qt.white)
            else:
                # Re-enable editing and set background to white
                ref_item.setFlags(ref_item.flags() | Qt.ItemIsEditable)
                ref_item.setBackground(Qt.white)
                ref_item.setForeground(Qt.black)

        # Force the table to refresh and update its view
        self.ui_components.reference_table.viewport().update()
    
    def update_routine(self, xopt_obj):
        self.xopt_obj = xopt_obj
        self.model_logic.update_xopt(self.xopt_obj)
        self.ui_components.update_vocs(self.xopt_obj.vocs)
        self.update_plot()

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Apply QtModern styles
    qtmodern.styles.light(app)

    # Initialize the main window
    window = BOPlotWidget(xopt_obj=X)

    # Wrap the window with QtModern's ModernWindow for the modern UI
    window.setWindowTitle("BO Visualizer")
    #window.resize(1400, 1050)

    window.show()

    sys.exit(app.exec_())
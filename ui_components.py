#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct  3 14:18:24 2024

@author: aaditya
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct  3 14:18:24 2024

@author: aaditya
"""

from PyQt5.QtWidgets import (
    QVBoxLayout, QHBoxLayout, QComboBox, QLabel, QGroupBox, QTableWidget, QTableWidgetItem, QSlider, QPushButton, QGridLayout, QCheckBox, QHeaderView
)
from PyQt5.QtCore import Qt

class UIComponents:
    def __init__(self, vocs):
        self.vocs = vocs

    def create_axis_layout(self):
        x_y_axis_layout = QGridLayout()
        x_label = QLabel("X-axis")
        y_label = QLabel("Y-axis")

        self.x_axis_combo = QComboBox()
        self.x_axis_combo.addItems(self.vocs.variable_names)

        self.y_axis_combo = QComboBox()
        self.y_axis_combo.addItems(self.vocs.variable_names)

        x_y_axis_layout.addWidget(QLabel("Select Variable"), 0, 0)
        x_y_axis_layout.addWidget(self.x_axis_combo, 0, 1)
        x_y_axis_layout.addWidget(x_label, 0, 2)

        x_y_axis_layout.addWidget(QLabel("Select Variable"), 1, 0)
        x_y_axis_layout.addWidget(self.y_axis_combo, 1, 1)
        x_y_axis_layout.addWidget(y_label, 1, 2)
        
        return x_y_axis_layout

    def create_reference_inputs(self):
        # Create a table with 2 columns: one for variables and one for reference points
        self.reference_table = QTableWidget(len(self.vocs.variable_names), 2)
        self.reference_table.setHorizontalHeaderLabels(["Variable", "Reference Point"])
        self.reference_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        self.ref_inputs = []  # List to store QTableWidgetItems for reference points

        for i, var_name in enumerate(self.vocs.variable_names):
            variable_item = QTableWidgetItem(var_name)
            self.reference_table.setItem(i, 0, variable_item)  # Set variable name in the first column
            variable_item.setFlags(variable_item.flags() & ~Qt.ItemIsEditable) # Make the variables non-editable

            reference_point_item = QTableWidgetItem("0.0")  # Default reference point
            self.ref_inputs.append(reference_point_item)
            self.reference_table.setItem(i, 1, reference_point_item)  # Set reference point in the second column

        return self.reference_table

    def create_options_section(self):
        options_group = QGroupBox("Options")
        options_layout = QVBoxLayout()

        self.acq_func_checkbox = QCheckBox("Acquisition Function")
        self.show_samples_checkbox = QCheckBox("Show Samples")
        self.show_prior_mean_checkbox = QCheckBox("Show Prior Mean")
        self.show_feasibility_checkbox = QCheckBox("Show Feasibility")

        options_layout.addWidget(self.acq_func_checkbox)
        options_layout.addWidget(self.show_samples_checkbox)
        options_layout.addWidget(self.show_prior_mean_checkbox)
        options_layout.addWidget(self.show_feasibility_checkbox)

        self.n_grid_slider = QSlider(Qt.Horizontal)
        self.n_grid_slider.setMinimum(1)
        self.n_grid_slider.setMaximum(100)
        self.n_grid_slider.setValue(50)
        self.n_grid_slider.setTickPosition(QSlider.TicksBelow)

        n_grid_label = QLabel("N_grid")
        n_grid_label.setAlignment(Qt.AlignCenter)
        
        options_layout.addWidget(n_grid_label)
        options_layout.addWidget(self.n_grid_slider)

        options_group.setLayout(options_layout)
        return options_group

    def create_buttons(self):
        button_layout = QHBoxLayout()
        self.logbook_button = QPushButton("Logbook")
        self.update_button = QPushButton("Update")

        button_layout.addWidget(self.logbook_button)
        button_layout.addWidget(self.update_button)

        self.logbook_button.setObjectName("logbook_button")
        self.update_button.setObjectName("update_button")
        
        return button_layout
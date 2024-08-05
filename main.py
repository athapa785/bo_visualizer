"""
Created on Fri Jul 12 09:51:08 2024

@author: aaditya
"""


import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QComboBox, QLineEdit,
    QCheckBox, QPushButton, QLabel, QGridLayout, QSizePolicy
)
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from xopt.generators.bayesian.visualize import visualize_generator_model
from model_visualization_example import X, vocs

class PlotWidget(QWidget):
    def __init__(self, parent=None, max_plot_vars=2):
        super().__init__(parent)
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        self.max_plot_vars = max_plot_vars  # Maximum number of variables to plot

        layout = QVBoxLayout()
        

        # Grid layout for variables, references, and checkboxes
        self.grid_layout = QGridLayout()
        self.variable_dropdowns = []
        self.ref_inputs = []
        self.include_checkboxes = []

        for i, var_name in enumerate(vocs.variable_names):
            # Variable dropdown
            var_dropdown = QComboBox()
            var_dropdown.addItems(vocs.variable_names)
            self.variable_dropdowns.append(var_dropdown)
            self.grid_layout.addWidget(QLabel(f"Variable {i+1}:"), i, 0)
            self.grid_layout.addWidget(var_dropdown, i, 1)

            # Reference input
            
            ref_input = QLineEdit("0.0")
            self.ref_inputs.append(ref_input)
            self.grid_layout.addWidget(QLabel("Reference:"), i, 2)
            self.grid_layout.addWidget(ref_input, i, 3)

            # Include checkbox 
            include_checkbox = QCheckBox(f"Include Variable {i+1}")
            include_checkbox.setChecked(i < self.max_plot_vars)  # Check first two by default
            include_checkbox.stateChanged.connect(self.update_ref_inputs)  # Connect to update function
            self.include_checkboxes.append(include_checkbox)
            self.grid_layout.addWidget(include_checkbox, i, 4)

        layout.addLayout(self.grid_layout)

        # Checkbox for acquisition function
        self.show_acq_checkbox = QCheckBox("Show Acquisition Function")
        layout.addWidget(self.show_acq_checkbox)

        # Update button
        update_button = QPushButton("Update Plot")
        update_button.clicked.connect(self.update_plot)
        layout.addWidget(update_button)

        # Plot area
        layout.addWidget(self.canvas)
        self.setLayout(layout)
        self.canvas.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.update_ref_inputs()  # Initialize reference inputs based on checkboxes
        
        

    def update_ref_inputs(self):
        checked_count = sum(cb.isChecked() for cb in self.include_checkboxes)
        for i, ref_input in enumerate(self.ref_inputs):
            ref_input.setEnabled(not self.include_checkboxes[i].isChecked())

    def update_plot(self):

        variable_names = [dropdown.currentText() for dropdown, checkbox in zip(self.variable_dropdowns, self.include_checkboxes) if checkbox.isChecked()]
        variable_names = [var for var in variable_names if var != ""]  # Filter out empty selections
        
        # Limit to a maximum of two variables
        variable_names = variable_names[:self.max_plot_vars] 

        # Create reference_point dictionary for non-selected variables only
        reference_point = {}
        for i, var in enumerate(X.vocs.variable_names):
            if var not in variable_names:
                ref_value = float(self.ref_inputs[i].text())
                reference_point[var] = ref_value
    
        self.figure.clear()
        fig, ax = visualize_generator_model(
            X.generator,
            variable_names=variable_names,
            reference_point=reference_point,
            show_acquisition=self.show_acq_checkbox.isChecked()
        )
    
        self.canvas.figure = fig
        self.canvas.draw()
        self.canvas.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PlotWidget()
    window.show()
    sys.exit(app.exec_())


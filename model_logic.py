#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct  3 14:18:45 2024

@author: aaditya
"""

class ModelLogic:
    def __init__(self, xopt_obj, vocs):
        self.xopt_obj = xopt_obj
        self.vocs = vocs

    def update_xopt(self, xopt_obj):
        if xopt_obj is not None:
            self.xopt_obj = xopt_obj
            self.vocs = xopt_obj.vocs
        else:
            print("Warning: xopt_obj is None in update_xopt")

    def get_reference_points(self, ref_inputs, variable_names):
        reference_point = {}
        for i, var in enumerate(self.vocs.variable_names):
            if var not in variable_names:
                ref_value = float(ref_inputs[i].text())
                reference_point[var] = ref_value
        return reference_point
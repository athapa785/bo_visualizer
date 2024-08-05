#!/usr/bin/env python
# coding: utf-8

# ## Constrained Bayesian Optimization
# In this tutorial we demonstrate the use of Xopt to perform Bayesian Optimization on a simple test problem subject to a single constraint.

# ## Define the test problem
# Here we define a simple optimization problem, where we attempt to minimize the sin
# function in the domian [0,2*pi], subject to a cos constraining function.


# Ignore all warnings
import warnings
warnings.filterwarnings("ignore")
import time
import math

from xopt.vocs import VOCS

# define variables, function objective and constraining function
vocs = VOCS(
    variables={"x0": [0., 2. * math.pi], "x1":[0., 2.*math.pi], "x2":[0., 2.*math.pi]},
    objectives={"f": "MINIMIZE"},
    constraints={"c": ["LESS_THAN", 0]}
)



# define a test function to optimize
import numpy as np

def test_function(input_dict):
    return {"f": np.sin(input_dict["x0"]*input_dict["x1"]),"c": np.cos
    (input_dict["x0"])}


# ## Create Xopt objects
# Create the evaluator to evaluate our test function and create a generator that uses
# the Expected Improvement acquisition function to perform Bayesian Optimization.


from xopt.evaluator import Evaluator
from xopt.generators.bayesian import ExpectedImprovementGenerator
from xopt import Xopt

evaluator = Evaluator(function=test_function)
generator = ExpectedImprovementGenerator(vocs=vocs)
X = Xopt(evaluator=evaluator, generator=generator, vocs=vocs)




# ## Generate and evaluate initial points
# To begin optimization, we must generate some random initial data points. The first call
# to `X.step()` will generate and evaluate a number of randomly points specified by the
#  generator. Note that if we add data to xopt before calling `X.step()` by assigning
#  the data to `X.data`, calls to `X.step()` will ignore the random generation and
#  proceed to generating points via Bayesian optimization.

# In[6]:


# call X.random_evaluate(n_samples) to generate + evaluate initial points
X.random_evaluate(n_samples=5)
X.generator.train_model()


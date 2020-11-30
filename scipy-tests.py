import numpy as np
from scipy.optimize import minimize
from TestFunctions import ackley_function, beale_function
import random

x0 = np.array([random.uniform(-2,2), random.uniform(-10,10)])

# Test with Nedler-Mead Simplex
#res = minimize(ackley_function, x0, method = 'Nelder-Mead')
#res = minimize(beale_function, x0, method = 'Nelder-Mead')

# Test with Powell Method
#res = minimize(ackley_function, x0, method = 'Powell')
#res = minimize(beale_function,x0, method='Powell')

# Test with Conjugate Gradient Method
#res = minimize(ackley_function, x0, method='CG')
#res = minimize(beale_function, x0, method='CG')

print(res)
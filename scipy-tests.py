import numpy as np
from scipy.optimize import minimize
from TestFunctions import ackley_function, beale_function
import random
import time

x0 = np.array([random.uniform(-2,2), random.uniform(-10,10)])

start = time.time()
# Test with Nedler-Mead Simplex
#res = minimize(ackley_function, x0, method = 'Nelder-Mead')
#res = minimize(beale_function, x0, method = 'Nelder-Mead')

# Test with Powell Method
#res = minimize(ackley_function, x0, method = 'Powell')
#res = minimize(beale_function,x0, method='Powell')

# Test with Conjugate Gradient Method
#res = minimize(ackley_function, x0, method='CG')
res = minimize(beale_function, x0, method='CG')

end = time.time()

print(res)
print("Elapsed Time: " + str(end - start))
from GASolver import GASolver
from TestFunctions import test_function_1, test_function_2,test_function_3, test_function_3_c1, test_function_3_c2,ackley_function,beale_function
import time

start = time.time()
# Example 1: Non-converging Question
#solver = GASolver(test_function_1,6)
#solver.solve((-5,5),50,20)

# Example 2: Converging Question
#solver2 = GASolver(test_function_2,2,None, False)
#solver2.solve([-5,5],50,25)

# Example 3: Converging Bounded Arora 3.9
#solver3 = GASolver(test_function_3,2,[test_function_3_c1, test_function_3_c2],False)
#solver3.solve([-1,1],75,15,50)

# Example 4: Ackley Function Orig 
#solver_ackley = GASolver(ackley_function,2, None, False)
#solver_ackley.solve([-2, 2],75,15)

# Example 5: Beale Function
solver_beale = GASolver(beale_function, 2, None, False, False)
solver_beale.solve([-2, 2], 75, 15, 50)

end = time.time()
print("Elapsed Time: " + str(end - start))
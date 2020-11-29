from GASolver import GASolver
import math

def test_function_1(x):
    return 5*x[0]+6*x[1]-3*x[2]+4*x[3]+5*x[4]-22*x[5]**2

def test_function_2(x):
    return (x[0]+x[1])/(3+x[0]**2+x[1]**2+x[0]*x[1])

def test_function_3(x):
    return x[0] * x[1]

def test_function_3_c1(x):
    return x[0] + x[1] ** 2

def test_function_3_c2(x):
    return x[0] ** 2 + x[1] ** 2 - 9

def ackley_function(x):
    a = 20
    b = 0.2
    c = 2*math.pi
    d = 2
    return -1 * a * math.exp(-1 * b * ((1/d) * (x[0] ** 2 + x[1] ** 2))**0.5) - math.exp((1/d)*(math.cos(c*x[0]) + math.cos(c*x[1]))) + a + math.exp(1)

def beale_function(x):
    return (1.5 - x[0] + x[0] * x[1]) ** 2 + (2.25 - x[0] + x[0] * x[1] ** 2) ** 2 + (2.625 - x[0] + x[0] * x[1] ** 3) ** 2

# Example 1: Non-converging Question
#solver = GASolver(test_function_1,6)
#solver.solve((-5,5),50,20)

# Example 2: Converging Question
#solver2 = GASolver(test_function_2,2,None, False)
#solver2.solve([-5,5],50,25)

# Example 3: Converging Bounded Arora 3.9
solver3 = GASolver(test_function_3,2,[test_function_3_c1, test_function_3_c2],False)
solver3.solve([-2,2],75,15,50)

# Example 4: Ackley Function Orig 
#solver_ackley = GASolver(ackley_function,2, None, False)
#solver_ackley.solve([-10, 10],50,15)

# Example 5: Beale Function
#solver_beale = GASolver(beale_function, 2, None, False)
#solver_beale.solve([-10, 10], 75, 15, 50)
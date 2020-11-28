from GASolver import GASolver

def test_function_1(x):
    return 5*x[0]+6*x[1]-3*x[2]+4*x[3]+5*x[4]-22*x[5]**2

def test_function_2(x):
    return (x[0]+x[1])/(3+x[0]**2+x[1]**2+x[0]*x[1])

def test_function_3(x):
    return 6*x[0]*x[1]*x[2]/(x[0]+2*x[1]+2*x[2])

#solver = GASolver(test_function_1,6)
#solver.solve((-5,5),50,20)

solver2 = GASolver(test_function_2,2, False)
solver2.solve([-5,5],50,25)

#solver3 = GASolver(test_function_3,3)
#solver3.solve([0,5],10,5)


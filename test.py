from docplex.mp.model import Model
import numpy as np
from knapsack import Knapsack
model = Model('Column generation')
W = 218
w = [81,70,68]
c = [1,1,1,1,1,1]
a = np.array([[1,0,0,0,1,2],[0,1,0,3,0,0],[0,0,1,0,2,0]])
rhs = [44,3,48]
x = model.continuous_var_list(len(c),0,name='x')
cons = []
for i in range(len(a[:,0])):
    cons.append(model.add_constraint(model.dot(x,a[i,:])>=rhs[i]))
model.minimize(model.sum(x))
model.solve()
print(model.objective_value)
print(model.dual_values(cons))
print(model.solution.get_all_values())
knapsack = Knapsack(W,w,model.dual_values(cons))
print(knapsack.solution)
print(knapsack.track)






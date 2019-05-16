# from docplex.mp.model import Model
# import numpy as np
# W = 218
# w = [81,70,68,77,74,53,88]
# demand = [44,30,48,22,31,29,27]
# m = 7
# a = np.array([[2.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0],[0., 3., 0., 0., 1., 0., 0.],[0., 0., 2., 0., 0., 0., 0.],[0., 0., 0., 1., 0., 0., 0.],[0., 0., 0., 0., 2, 0., 0.],[1., 0., 0., 1., 0., 4., 0.],[0., 0., 0., 1., 0., 0., 2.]])
# model = Model('RLPM')
# x = model.continuous_var_list(m,0,name='x')
# constraints = []
# for i in range(m):
#     constraints.append(model.add_constraint(model.dot(x,a[i,:]) >= demand[i]))
# model.minimize(model.sum(x))
# model.solve()
# prime = model.solution.get_all_values()
# objective = model.objective_value
# dual = model.dual_values(constraints)
# print(prime)
# print(objective)
import numpy as np
c = np.array([4,6,7])
a = np.array([[1,2,3,4],[2,3,5,6],[3,4,6,7]])
print(a.shape)
b = [1,2,3]
for i in range(len(a[0])):
    if all(a[:,i] == c):
        print('equal')
        a = np.delete(a,i,axis=1)
        break
print(a)







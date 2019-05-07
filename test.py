# from docplex.mp.model import Model
# model = Model('Column generation')
# a = [[1,0,0],[0,1,0],[0,0,1]]
# c = [1] * 3
# rhs = [44,3,48]
# x = model.continuous_var_list(3,0,name='x')
# print(model)
# model.clear()
# x = model.continuous_var_list(3,0,name='x')
# print(model)
# cts = []
# for i in range(3):
#     ct = model.add_constraint(model.dot(x,a[i]) <= rhs[i])
#     cts.append(ct)
# model.maximize(model.dot(x,c))
# model.solve()
# dual = model.dual_values(cts)
# a = model.solution.get_all_values()
# print(a)
def f():
    return break

for i in range(10):
    if i < 7:
        print(i)
    else:
        f()


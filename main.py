from docplex.mp.model import Model
import numpy as np
from knapsack import Knapsack

class Column_generation():

    def __init__(self):

        self.W = 218
        # 重复且替换导致一行无变量
        # self.w = [81,70,68,77,74,53,88,23,45,59,65,71,56,106,91,87,82,85,91]
        # self.demand = [44,30,48,22,31,29,37,23,12,43,42,33,22,32,17,36,27,45,41]
        self.w = [70,68,77,33,91,86]
        self.demand = [30,48,12,22,17,31]
        # self.w = [68,77,33,90,86,55,74,45,43,75,17,91,76,84,24,26,31,35,38,76,61,64,68]
        # self.demand = [37,48,12,22,17,31,23,80,25,13,45,28,54,61,37,54,84,12,18,79,92,12,30]
        self.m = len(self.w)
        self.col_num = self.m
        self.objective = float('inf')

    
    def initial(self):
        self.a = np.zeros((self.m,self.m))
        for i in range(self.m):
            self.a[i,i] = int(self.W / self.w[i])


    def rlpm(self):
        model = Model('RLPM')
        x = model.continuous_var_list(len(self.a[0]),0,name='x')
        constraints = []
        for i in range(self.m):
            constraints.append(model.add_constraint(model.dot(x,self.a[i,:]) >= self.demand[i]))
        model.minimize(model.sum(x))
        model.solve()
        self.prime = model.solution.get_all_values()
        self.objective = model.objective_value
        self.dual = model.dual_values(constraints)
        # print(np.round(self.prime,2))
        # print(np.round(self.dual,2))
        # print(model.reduced_costs(x))
        # print(model.slack_values(constraints))
        # return self.objective
    
    def change_col(self,col):
        theta = np.zeros(self.m)
        for i in range(self.m):
            if col[i] > 0:
                theta[i] = self.demand[i] / col[i]
            else:
                theta[i] = float('inf')
        # if col not in self.a.T:
        if sorted(self.prime,reverse=True)[self.m - 1] > 0:
            self.a = self.a[:,np.array(self.prime) > 0]
            self.test()
            out_basis = np.argmin(theta)
            self.a[:,out_basis] = col
            self.test()
        else:
            self.a = np.c_[self.a,col]
                # print(col)
        # else:
        #     model = Model('feasible problem')
        #     y = model.integer_var_list(self.m,0,name='y')
        #     model.add_constraint_(model.dot(y,self.dual) >= 1.01)
        #     model.add_constraint_(model.dot(y,self.w) <= self.W)
        #     model.minimize(0)
        #     model.solve()
        #     self.change_col(model.solution.get_all_values())
    
    def test(self):
        for i,j in enumerate(self.a):
            if all(j == 0):
                col = np.zeros(self.m)
                col[i] = int(self.W / self.w[i])
                self.a = np.c_[self.a,col]

    def run(self):
        self.initial()
        while 1:
            temp = self.objective
            self.rlpm()
            if self.objective < temp:
                pass
            else:
                print(self.objective)
                return self.a,self.prime
            knapsack = Knapsack(self.W,self.w,self.dual)
            if knapsack.objective > 1:
                self.change_col(knapsack.solution)
            else:
                print(self.objective)
                return self.a,self.prime

if __name__=='__main__':
    column_generation = Column_generation()
    # column_generation.initial()
    # column_generation.a[1] = 0
    # print(column_generation.a)
    # column_generation.test()
    # print('#'*20)
    # print(column_generation.a)
    a,x = column_generation.run()
    print(a)
    print(x)

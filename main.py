from docplex.mp.model import Model
import numpy as np
from knapsack import Knapsack

class Column_generation():

    def __init__(self):

        self.W = 218
        # self.w = [81,70,68,77,74,53,88,23,45,59,65,71,56,106,91,87,82,85,91]
        self.w = [48,23,45,59,65,71,56,106,91]
        # self.demand = [44,30,48,22,31,29,37,23,12,43,42,33,22,32,17,36,27,45,41]
        self.demand = [37,23,12,43,42,33,22,32,17]
        self.m = len(self.w)
        self.col_num = self.m

    
    def initial(self):
        self.a = np.zeros((self.m,self.col_num))
        for i in range(self.m):
            self.a[i,i] = int(self.W / self.w[i])
        self.substitute_col_num = 0
        self.add_col_num = 0


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
        # print(model.reduced_costs(x))
        # print(model.slack_values(constraints))
    
    def change_col(self,col):
        if sorted(self.prime,reverse=True)[self.m - 1] > 0:
            # self.a = self.a[:,np.array(self.prime) > 0]
            theta = np.zeros(self.m)
            for i in range(self.m):
                if col[i] > 0:
                    theta[i] = self.demand[i] / col[i]
                else:
                    theta[i] = float('inf')
            out_basis = np.argmin(theta)
            self.a[:,out_basis] = col
            self.substitute_col_num += 1
            print('替换')
        else:
            self.a = np.c_[self.a,col]
            self.add_col_num += 1
            print('添加')

    def run(self):
        self.initial()
        while 1:
            self.rlpm()
            knapsack = Knapsack(self.W,self.w,self.dual)
            if knapsack.objective > 1:
                self.change_col(knapsack.solution)
            else:
                # print(self.substitute_col_num)
                # print(self.add_col_num)
                print(self.objective)
                # print(self.dual)
                return self.a,self.prime

if __name__=='__main__':
    column_generation = Column_generation()
    a,x = column_generation.run()
    print(a)
    print(x)

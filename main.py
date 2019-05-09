from docplex.mp.model import Model
import numpy as np
from knapsack import Knapsack

class Column_generation():

    def __init__(self):

        self.W = 218
        self.w = [81,70,68,77,33,9,86,55,74,83]
        self.demand = [44,3,48,12,22,17,31,23,8,11]
        # self.W = 600
        # self.w = np.random.randint(10,200,80)
        # self.demand = np.random.randint(10,200,80)
        self.m = len(self.w)
        self.col_num = self.m

    
    def initial(self):
        self.a = np.zeros((self.m,self.col_num))
        for i in range(self.m):
            self.a[i,i] = int(self.W / self.w[i])
        self.substitute_col_num = 0


    def rlpm(self):
        model = Model('RLPM')
        x = model.continuous_var_list(self.col_num,0,name='x')
        constraints = []
        for i in range(self.m):
            constraints.append(model.add_constraint(model.dot(x,self.a[i,:]) >= self.demand[i]))
        model.minimize(model.sum(x))
        model.solve()
        self.prime = model.solution.get_all_values()
        self.objective = model.objective_value
        self.dual = model.dual_values(constraints)
    
    def substitute_col(self,col):
        theta = np.zeros(self.m)
        for i in range(self.m):
            if col[i] > 0:
                theta[i] = self.demand[i] / col[i]
            else:
                theta[i] = float('inf')
        out_basis = np.argmin(theta)
        self.a[:,out_basis] = col
        self.substitute_col_num += 1

    def run(self):
        self.initial()
        while 1:
            self.rlpm()
            knapsack = Knapsack(self.W,self.w,self.dual)
            if knapsack.objective > 1:
                self.substitute_col(knapsack.solution)
            else:
                print(self.substitute_col_num)
                print(self.objective)
                print(self.dual)
                return self.a,self.prime

if __name__=='__main__':
    column_generation = Column_generation()
    a,x = column_generation.run()
    print(a)
    print(x)

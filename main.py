from docplex.mp.model import Model
import numpy as np
from knapsack import Knapsack

class Column_generation():

    def __init__(self):

        self.W = 218
        self.w = [81,70,68,77,33,9,86,55,74,83]
        self.demand = [44,3,48,12,22,17,31,23,8,11]
        self.m = len(self.w)
        self.col_num = self.m

    
    def initial(self):
        self.a = np.zeros((self.m,self.col_num))
        for i in range(self.m):
            self.a[i,i] = int(self.W / self.w[i])
        self.substitute_col_num = 0


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
    
    def add_col(self,col):
        self.a = np.c_[self.a,col]

    def run(self):
        self.initial()
        while 1:
            self.rlpm()
            knapsack = Knapsack(self.W,self.w,self.dual)
            if knapsack.objective > 1:
                self.add_col(knapsack.solution)
            else:
                print(self.objective)
                return self.a,self.prime

if __name__=='__main__':
    column_generation = Column_generation()
    a,x = column_generation.run()
    print(a)
    print(x)

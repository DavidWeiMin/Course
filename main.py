# code must be tested by the following examples:
# W = 12, w1 = 1, w2 = 2, n1 = 6, n2 = 3
# W = 12, w1 = 1, w2 = 2, n1 = 4, n2 = 4
# W = 1200, w1 = 10, w2 = 20, n1 = 60, n2 = 30
# W = 1200, w1 = 10, w2 = 20, n1 = 40, n2 = 40
# W = 100, w1 = 11, w2 = 41, n1 = 73, n2 = 13
# W = 100, w1 = 23, w2 = 29, n1 = 43, n2 = 43
# W = 100, w1 = 23, w2 = 29, n1 = 73, n2 =13
# W = 100, w1 = 11, w2 = 41, n1 = 43, n2 = 43

from docplex.mp.model import Model
import numpy as np
from knapsack import Knapsack

class Column_generation():

    def __init__(self):

        # self.W = 1200
        # self.w = [17,15,16,69,74,46,33,57,22,80]
        # self.demand = [22,25,12,8,13,31,4,8,9,10]
        self.W = 300
        self.w = np.random.randint(10,200,80)
        self.demand = np.random.randint(10,200,80)
        self.m = len(self.w)
        self.col_num = self.m

    
    def initial(self):
        # self.a = np.identity(self.m)
        self.a = np.zeros((self.m,self.col_num))
        for i in range(self.m):
            self.a[i,i] = int(self.W / self.w[i])
        model = Model('RLPM')
        x = model.continuous_var_list(self.col_num,0,name='x')
        constraints = []
        for i in range(self.m):
            constraints.append(model.add_constraint(model.dot(x,self.a[i,:]) >= self.demand[i]))
        model.minimize(model.dot(x,[1]*self.col_num))
        model.solve()
        self.objective = model.objective_value
        self.dual = model.dual_values(constraints)
        self.descent = True


    def rlpm(self,flag=None):
        # self.model.clear()
        model = Model('RLPM')
        x = model.continuous_var_list(self.col_num,0,name='x')
        constraints = []
        for i in range(self.m):
            constraints.append(model.add_constraint(model.dot(x,self.a[i,:]) >= self.demand[i]))
        model.minimize(model.dot(x,[1]*self.col_num))
        model.solve()
        objective = model.objective_value
        if flag:
            self.prime = model.solution.get_all_values()
        if objective < self.objective:
            self.objective = objective
            self.dual = model.dual_values(constraints)
            return True
        else:
            return False
    
    def add_col(self,col):
        self.a = np.c_[self.a,col]

    def run(self):
        self.initial()
        while 1:
            if self.descent:
                knapsack = Knapsack(self.W,self.w,self.dual)
                if knapsack.solution > 1:
                    self.add_col(knapsack.track)
                    self.col_num += 1
                else:
                    self.rlpm(flag=1)
                    return self.a,self.prime
            else:
                self.rlpm(flag=1)
                return self.a,self.prime
            self.descent = self.rlpm()

if __name__=='__main__':
    column_generation = Column_generation()
    a,x = column_generation.run()
    print(a.shape)
    print(x)

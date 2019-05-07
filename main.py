from docplex.mp.model import Model
import numpy as np
from knapsack import Knapsack

class Column_generation():

    def __init__(self):

        self.W = 218
        self.w = [81,70,68]
        self.demand = [44,3,48]
        # self.W = 600
        # self.w = np.random.randint(10,200,80)
        # self.demand = np.random.randint(10,200,80)
        self.m = len(self.w)
        self.col_num = self.m

    
    def initial(self):
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
        self.substitute_col_num = 0


    def rlpm(self,flag=None):
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
        if objective < self.objective - 1e-3:
            self.objective = objective
            self.dual = model.dual_values(constraints)
            return True
        else:
            return False
    
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
            if self.descent:
                knapsack = Knapsack(self.W,self.w,self.dual)
                if knapsack.solution > 1:
                    self.substitute_col(knapsack.track)
                else:
                    self.rlpm(flag=1)
                    print(self.substitute_col_num)
                    print(self.objective)
                    print(self.dual)
                    return self.a,self.prime
            else:
                self.rlpm(flag=1)
                print(self.substitute_col_num)
                print(self.objective)
                print(self.dual)
                return self.a,self.prime
            self.descent = self.rlpm()

if __name__=='__main__':
    column_generation = Column_generation()
    a,x = column_generation.run()
    print(a)
    print(x)

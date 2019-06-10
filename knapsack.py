"""
参考网址：
0-1背包：https://www.jianshu.com/p/25f4a183ede5?utm_campaign=maleskine&utm_content=note&utm_medium=seo_notes&utm_source=recommendation
完全背包：https://www.jianshu.com/p/7a4e6071bc02
代码主要参考(源代码有错误)：https://blog.csdn.net/w113691/article/details/81749364
"""

class Knapsack():
    """背包问题
    """

    def __init__(self,c=218,w=[81,70,68],v=[1,1/3,1/3],mode=1):
        """初始化背包问题的基本参数
        
        Keyword Arguments:
            c {int} -- [背包容量] (default: {218})
            w {list} -- [可选物品重量向量] (default: {[81,70,68]})
            v {list} -- [可选物品价值向量] (default: {[1,1,1/3]})
            mode {int} -- [0:0-1背包;1:完全背包] (default: {1})
        """
        self.c = c
        self.w = w
        self.v = v
    
    @property # 属性修饰器
    def objective(self):
        """求解背包能装下的最大总价值
        
        Returns:
            [float] -- [最大总价值]
        """
        self.V = [[0] * (self.c + 1) for i in range(len(self.w) + 1)]
    
        for i in range(1, len(self.w) + 1):
            for j in range(1, self.c + 1):
                if j >= self.w[i - 1]:
                    self.V[i][j] = max(self.V[i - 1][j], self.V[i][j - self.w[i - 1]] + self.v[i - 1])
                else:
                    self.V[i][j] = self.V[i - 1][j]
        return max(self.V[-1])
    
    @property
    def solution(self):
        """[返回最优时每个物品的装载量]
        
        Returns:
            [list] -- [每个物品的装载量]
        """
        x = [0] * len(self.w)
        c = self.c
        while c > min(self.w):
            for i in range(len(self.w), 0, -1):
                if self.V[i][c] != self.V[i - 1][c]:
                    x[i-1] += 1
                    c = c - self.w[i - 1]
                    break
            else:#最小重量的物品的价值可能为0
                break
        return x
 
if __name__ == '__main__':
    # 测试
    knapsack = Knapsack(218,[70, 68, 77, 33, 9, 86, 55, 74],[0.3333333333333333, 0.3333333333333333, 0.375, 0.125, 0, 0.5, 0.25, 0.375])
    print(knapsack.objective)
    print(knapsack.solution)
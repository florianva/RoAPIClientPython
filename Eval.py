class Optimisation:

    def __init__(self, filename):
        with open(filename, "r") as f:
            self.n = int(f.readline())
            s = f.readline().split(' ')
            self.w = [ float(i) for i in s ]
            s = f.readline().split(' ')
            self.x = [ int(i) for i in s ]

    def eval(self):
        r = 0
        for i in range(self.n):
            r += self.w[i] * self.x[i]
        return r

    def newSolution(self, solution):
        s = solution.split('-')
        self.x = [int(i) for i in s]

    def __str__(self):
        s = str(self.x[0])
        for i in range(1,len(self.x)):
            s += "-" + str(self.x[i])
        return(s)


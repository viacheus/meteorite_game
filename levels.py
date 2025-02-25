import random


class Problem:
    def __init__(self, complexity):
        self.complexity = complexity


class SumProblem(Problem):
    def __init__(self, complexity):
        super().__init__(complexity)
        self.sign = "+"

    def get_problem(self):
        a = random.randint(1, self.complexity * 4)
        b = random.randint(1, self.complexity * 4)
        return (f"{a} + {b}", a + b)


class SubProblem(Problem):
    def __init__(self, complexity):
        super().__init__(complexity)
        self.sign = "-"

    def get_problem(self):
        a = random.randint(1, self.complexity * 4)
        b = random.randint(1, a)
        return (f"{a} - {b}", a - b)


class Level:
    def __init__(self, *problems):
        self.problems = problems

    def get_problem(self):
        problem = random.choice(self.problems)
        return problem.get_problem()


levels = [
    Level(SumProblem(1)),
    Level(SumProblem(5), SubProblem(5)),
    Level(SumProblem(10), SubProblem(10)),
    Level(SumProblem(15), SubProblem(15)),
    Level(SumProblem(30), SubProblem(30))
]

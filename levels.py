import random


class Problem:
    def __init__(self, complexity):
        self.complexity = complexity


class SumProblem(Problem):
    def __init__(self, complexity):
        super().__init__(complexity)
        self.sign = "+"

    def get_problem(self):
        a = random.randint(0, self.complexity * 3)
        b = random.randint(0, self.complexity * 3)
        return (f"{a} + {b}", a + b)


class SubProblem(Problem):
    def __init__(self, complexity):
        super().__init__(complexity)
        self.sign = "-"

    def get_problem(self):
        a = random.randint(0, self.complexity * 3)
        b = random.randint(0, a)
        return (f"{a} - {b}", a - b)


class Level:
    def __init__(self, *problems):
        self.problems = problems

    def get_problem(self):
        problem = random.choice(self.problems)
        return problem.get_problem()


levels = [
    Level(SumProblem(1)),
    Level(SumProblem(1), SubProblem(1)),
    Level(SumProblem(2), SubProblem(2)),
    Level(SumProblem(3), SubProblem(3)),
    Level(SumProblem(4), SubProblem(4))
]

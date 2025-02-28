import random
from database import get_settings


class Problem:
    def __init__(self, complexity):
        self.complexity = complexity


class SumProblem(Problem):
    def __init__(self, complexity):
        super().__init__(complexity)
        self.sign = "+"

    def get_problem(self):
        a = random.randint(1, self.complexity * 2)
        b = random.randint(1, self.complexity * 2)
        return (f"{a} + {b}", a + b)


class SubProblem(Problem):
    def __init__(self, complexity):
        super().__init__(complexity)
        self.sign = "-"

    def get_problem(self):
        a = random.randint(1, self.complexity * 2)
        b = random.randint(1, a)
        return (f"{a} - {b}", a - b)


class MulProblem(Problem):
    def __init__(self, complexity):
        super().__init__(complexity)
        self.sign = "*"

    def get_problem(self):
        a = random.randint(1, self.complexity)
        b = random.randint(1, self.complexity)
        return (f"{a} × {b}", a * b)


class DivProblem(Problem):
    def __init__(self, complexity):
        super().__init__(complexity)
        self.sign = "/"

    def get_problem(self):
        b = random.randint(1, self.complexity)
        a = b * random.randint(1, self.complexity)
        return (f"{a} ÷ {b}", a // b)


class Level:
    def __init__(self, db_conn, level_number):
        self.db_conn = db_conn
        self.level_number = level_number
        self.problems = self.load_problems()
        self.last_settings = None

    def load_problems(self):
        settings = get_settings(self.db_conn, self.level_number)
        self.last_settings = settings

        if not settings:
            return [SumProblem(self.level_number * 2)]

        complexity = settings[5] if settings[5] else (self.level_number * 2)
        problems = []

        if settings[1]:
            problems.append(SumProblem(complexity))
        if settings[2]:
            problems.append(SubProblem(complexity))
        if settings[3]:
            problems.append(MulProblem(complexity))
        if settings[4]:
            problems.append(DivProblem(complexity))

        if not problems:
            problems.append(SumProblem(complexity))

        return problems

    def get_problem(self):
        current_settings = get_settings(self.db_conn, self.level_number)
        if current_settings != self.last_settings:
            self.problems = self.load_problems()

        problem = random.choice(self.problems)
        return problem.get_problem()


def create_levels(db_conn):
    return [Level(db_conn, i + 1) for i in range(5)]

from functools import reduce

class College:
    "Holds the name, admissions probability, and utility associated with a college."
    def __init__(self, name, f, t):
        self.name = name
        self.f = f
        self.t = t
        assert 0 < f <= 1, "Need 0 < f ≤ 1"
        assert 0 <= t, "Need 0 ≤ t"

    def ft(self):
        return self.f * self.t

    def discount(self, c):
        "Update t to reflect the marginal utility relative to a portfolio containing c. Returns a college."
        if self.t < c.t:
            return College(self.name, self.f, self.t * (1 - c.f))
        else:
            return College(self.name, self.f, self.t - c.ft())


def _application_order(colleges: list) -> tuple:
    "Optimal order in which to apply to the listed schools, and the associated portfolio valuations."
    m = len(colleges)

    best_idx = reduce(
        lambda i, j: i if colleges[i].ft() >= colleges[j].ft() else j,
        range(len(colleges))
    )

    best_c = colleges[best_idx]

    x = []
    v = [best_c.ft()]

    for j in range(m-1):
        x.append(best_c.name)
        if j > 0:
            v.append(v[-1] + best_c.ft())

        new_best_idx = 0
        new_best_c = colleges[0]

        for i in range(best_idx):
            colleges[i] = colleges[i].discount(best_c)
            if colleges[i].ft() >= new_best_c.ft():
                new_best_idx = i
                new_best_c = colleges[i]
        
        for i in range(best_idx, len(colleges)-1):
            colleges[i] = colleges[i+1].discount(best_c)
            if colleges[i].ft() >= new_best_c.ft():
                new_best_idx = i
                new_best_c = colleges[i]

        best_idx = new_best_idx
        best_c = colleges[new_best_idx]

        colleges.pop()

    x.append(best_c.name)
    v.append(v[-1] + best_c.ft())

    return x, v


def application_order(names: list, f: list, t: list) -> tuple:
    "Optimal order in which to apply to the listed schools, and the associated portfolio valuations."
    return _application_order(
        [College(*c) for c in zip(names, f, t)]
    )


if __name__ == "__main__":
    names = "Mercury Venus Mars Jupiter Saturn Uranus Neptune Pluto".split()
    f = [0.39, 0.33, 0.24, 0.24, 0.05, 0.03, 0.1, 0.12]
    t = [200, 250, 300, 350, 400, 450, 500, 550]
    x, v = application_order(names, f, t)
    print(x)
    print(v)

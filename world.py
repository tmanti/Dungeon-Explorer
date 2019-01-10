from opensimplex import OpenSimplex
import random

class world:
    def __init__(self, seed=random.randint(1, 100000)):
        self.seed = seed
        self.gen = OpenSimplex(seed=self.seed)

    def noise(self, x, y):
        self.gen.noise2d(x=x, y=y)

    def returnWorldData(self):
        return {"seed":self.seed}
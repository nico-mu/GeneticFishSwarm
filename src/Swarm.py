import random
from time import time, sleep
from config import FishConstants, WindowConstants
from Fish import Fish


class Swarm:

    random.seed(time())

    def __init__(self, root, canvas, terrain) -> None:
        self.terrain = terrain
        self.root = root
        self.canvas = canvas
        self.fishSwarm = self.spawnSwarm()

    def spawnSwarm(self):
        MATING_POOL = [
            [self.__getRandomDnaString()
             for _ in range(FishConstants.max_lifespan)]
            for _ in range(random.randint(100, 500))]
        return [Fish(canvas=self.canvas, DNA=random.choice(MATING_POOL), terrain=self.terrain)
                for _ in range(FishConstants.number_of_fish)]

    def simulateSwarm(self):
        for _ in range(FishConstants.max_lifespan):
            for fish in self.fishSwarm:
                fish.draw()
                for k, v in self.terrain.items():
                    overlappingObject = self.canvas.find_overlapping(
                        v[0], v[1], v[2], v[3])
                    if fish.getId() in overlappingObject:
                        if k == 1:
                            fish.setAlive(True)
                            fish.setFinished(True)
                        else:
                            fish.setAlive(False)
                            fish.setFinished(True)
            self.canvas.pack()
            self.root.update_idletasks()
            self.root.update()
            sleep(1 / WindowConstants.FPS)

    def mating(self):
        newFishSwarm = [None] * len(self.fishSwarm)
        MATING_POOL = []
        bestReward = max([fish.calculateReward() for fish in self.fishSwarm])
        for fish in self.fishSwarm:
            fish.clear()
            likelihood = (fish.calculateReward() / bestReward) * 100
            [MATING_POOL.append(fish.getDNA())
             for _ in range(int(likelihood))]

        for i in range(len(self.fishSwarm)):
            retry = 100
            parentA = random.choice(MATING_POOL)
            parentB = random.choice(MATING_POOL)
            while parentA == parentB and retry > 0:
                parentB = random.choice(MATING_POOL)
                retry -= 1
            child = self.__mutate(parentA[:len(parentA)//2] +
                                  parentB[len(parentB)//2:])
            newFishSwarm[i] = Fish(
                canvas=self.canvas, DNA=child, terrain=self.terrain)
        self.fishSwarm = newFishSwarm

    def runSwarm(self):
        self.simulateSwarm()
        self.mating()

    def __mutate(self, dna):
        for i in range(len(dna)):
            if random.random() < 0.01:
                dna[i] = [dna[i][0], self.__getRandomDnaString()[1]]
            if random.random() < 0.01:
                dna[i] = [self.__getRandomDnaString()[0], dna[i][1]]
        return dna

    def __getRandomDnaString(self):
        return [random.uniform(-FishConstants.max_velocity, FishConstants.max_velocity), random.uniform(-FishConstants.max_drift, FishConstants.max_drift)]

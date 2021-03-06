import random
from time import sleep, time

from config import FishConstants, WindowConstants
from Fish import Fish


class Swarm:

    random.seed(time())
    GENERATION = 1

    def __init__(self, root, canvas, doTrackLine, terrain, numberOfFish, maxLifeSpan, mutationRate) -> None:
        self.terrain = terrain
        self.root = root
        self.maxLifeSpan = maxLifeSpan
        self.doTrackLine = doTrackLine
        self.numberOfFish = numberOfFish
        self.canvas = canvas
        self.deltaTime = 0
        self.trackLine = 0
        self.fishSwarm = self.__spawnSwarm()
        self.mutationRate = mutationRate

    def getBestDNA(self):
        return self.__calculateFitestFish().getDNA()

    def simulateSwarm(self):
        for _ in range(int(self.maxLifeSpan.get())):
            for fish in self.fishSwarm:
                if fish.finished:
                    continue
                fish.draw()
                for k, v in self.terrain.items():
                    overlappingObject = self.canvas.find_overlapping(
                        v[0], v[1], v[2], v[3])
                    if fish.getId() in overlappingObject:
                        if k == 1:
                            fish.setAlive(True)
                            fish.setFinished(True)
                            self.__calculateDeltaTime(fish)
                        else:
                            fish.setAlive(False)
                            fish.setFinished(True)
            self.__clearTrackingLine()
            if self.doTrackLine.get():
                self.__renderTrackingLine(
                    self.__calculateFitestFish().getCenter())
            self.canvas.grid(row=2)
            self.root.update_idletasks()
            self.root.update()
            sleep(1 / WindowConstants.FPS)

    def mating(self):
        newFishSwarm = [None] * int(self.numberOfFish.get())
        MATING_POOL = []
        bestReward = max([fish.calculateReward() for fish in self.fishSwarm])
        for fish in self.fishSwarm:
            fish.clear()
            likelihood = (fish.calculateReward() / bestReward) * 100
            [MATING_POOL.append(fish.getDNA())
             for _ in range(int(likelihood))]

        for i in range(int(self.numberOfFish.get())):
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

    def run(self):
        self.__renderTitle()
        self.deltaTime = 0
        self.simulateSwarm()
        self.mating()
        self.GENERATION += 1

    def resetSwarm(self):
        for fish in self.fishSwarm:
            fish.clear()
        self.fishSwarm = self.__spawnSwarm()

    def __calculateFitestFish(self):
        currentReward = 0
        prevReward = 0
        res = None
        for fish in self.fishSwarm:
            currentReward = fish.calculateReward()
            if currentReward > prevReward:
                res = fish
                prevReward = currentReward
        return res

    def __calculateDeltaTime(self, fish):
        if fish.isAlive and fish.finished:
            if self.deltaTime != 0:
                self.deltaTime = (self.deltaTime + fish.lifecircle) // 2
            else:
                self.deltaTime = fish.lifecircle
        self.__renderTitle()

    def __mutate(self, dna):
        for i in range(len(dna)):
            if random.random() < float(self.mutationRate.get()):
                dna[i] = [dna[i][0], self.__getRandomDnaString()[1]]
            if random.random() < float(self.mutationRate.get()):
                dna[i] = [self.__getRandomDnaString()[0], dna[i][1]]
        return dna

    def __getRandomDnaString(self):
        return [random.uniform(-FishConstants.max_velocity, FishConstants.max_velocity), random.uniform(-FishConstants.max_drift, FishConstants.max_drift)]

    def __clearTrackingLine(self):
        self.canvas.delete(self.trackLine)

    def __renderTrackingLine(self, pos):
        self.trackLine = self.canvas.create_line(
            pos[0],
            pos[1],
            WindowConstants.goal_delta_X,
            WindowConstants.goal_delta_Y,
            width=WindowConstants.tracking_line_width,
            fill=WindowConstants.tracking_line_color
        )

    def __renderTitle(self):
        self.root.title(
            f"Fish Generation : {self.GENERATION} | Average completion time : {self.deltaTime}")

    def __spawnSwarm(self):
        MATING_POOL = [
            [self.__getRandomDnaString()
             for _ in range(int(self.maxLifeSpan.get()))]
            for _ in range(random.randint(100, 500))]
        return [Fish(canvas=self.canvas, DNA=random.choice(MATING_POOL), terrain=self.terrain)
                for _ in range(int(self.numberOfFish.get()))]

import math

from config import FishConstants, WindowConstants


class Fish():

    def __init__(self, canvas, DNA, terrain) -> None:
        # DNA[0] = acceleration
        # DNA[1] = drift
        self.alive = True
        self.finished = False
        self.lifecircle = 0

        self.visual = 0
        self.canvas = canvas
        self.terrain = terrain
        self.velocity = 0
        self.acceleration = 0
        self.drift = 270
        self.DNA = DNA
        self.reset()
        self.__render()

    def draw(self):
        if self.alive and not self.finished:
            # a_list = [0, 5]
            # distribution = [.6, .4]
            # self.drift = random.choices(a_list, distribution)[0]
            self.clear()
            self.__calculate()
            self.__render()
            self.lifecircle += 1

    def clear(self):
        self.canvas.delete(self.visual)

    def reset(self):
        # pos[0] and pos[1] = front
        # pos[2] and pos[3] = back
        self.pos = [
            FishConstants.start_x,
            FishConstants.start_y + FishConstants.height,
            FishConstants.start_x,
            FishConstants.start_y
        ]

    def calculateReward(self):

        distanceMax = math.sqrt(
            (WindowConstants.goal_delta_X - WindowConstants.width)**2 + (WindowConstants.goal_delta_Y - WindowConstants.height)**2)
        if self.finished and self.alive:
            return (distanceMax) * 5 + (FishConstants.max_lifespan - self.lifecircle) * 50
        else:
            distanceGoal = self.__calculateGoalDistance()
            if self.alive:
                return distanceMax - distanceGoal
            else:
                return (distanceMax - distanceGoal) / 5

    def __calculateGoalDistance(self):
        return math.sqrt((WindowConstants.goal_delta_X - self.pos[0])**2 + (WindowConstants.goal_delta_Y - self.pos[1])**2)

    def getCenter(self):
        return [(self.pos[2] + self.pos[0]) / 2, (self.pos[3] + self.pos[1]) / 2]

    def isAlive(self):
        return self.alive

    def getDNA(self):
        return self.DNA

    def setAlive(self, alive):
        self.alive = alive

    def setFinished(self, finished):
        self.finished = finished

    def getId(self):
        return self.visual

    def __calculate(self):
        # x directions: positive number right, negative number left
        # y directions: positive numver down, negative number up
        # drift: left or right
        # velocity: up or down
        self.acceleration += self.DNA[self.lifecircle][0]
        self.drift += self.DNA[self.lifecircle][1]
        self.velocity += self.acceleration

        degree = (self.drift * math.pi) / 180

        # use sin and cos to simulate ciruclar movement
        if degree != 0:
            newX2 = self.pos[2] + self.velocity * math.cos(degree)
            newY2 = self.pos[3] + self.velocity * math.sin(degree)
            newY1 = newY2 - \
                (FishConstants.height * math.sin(degree))
            newX1 = newX2 - \
                (FishConstants.height * math.cos(degree))

            bounce = self.__checkBounce(newX1, newY1, self.pos[0], self.pos[1])
            if type(bounce) == bool:
                self.pos[3] = newY2
                self.pos[2] = newX2
                self.pos[1] = newY1
                self.pos[0] = newX1

        else:
            newX = self.pos[2] + (self.pos[2] - self.pos[0]) / \
                FishConstants.height * self.velocity
            newY = self.pos[3] + (self.pos[3] - self.pos[1]) / \
                FishConstants.height * self.velocity
            newX2 = self.pos[0] - (self.pos[0] - self.pos[2]) / \
                FishConstants.height * self.velocity
            newY2 = self.pos[1] - (self.pos[1] - self.pos[3]) / \
                FishConstants.height * self.velocity

            bounce = self.__checkBounce(newX, newY, self.pos[0], self.pos[1])
            if type(bounce) == bool:
                self.pos[0] = newX2
                self.pos[1] = newY2
                self.pos[2] = newX
                self.pos[3] = newY

        self.acceleration = 0

    def __render(self):
        self.visual = self.canvas.create_line(
            self.pos[0],
            self.pos[1],
            self.pos[2],
            self.pos[3],
            width=FishConstants.width,
            fill=FishConstants.color
        )

    def __checkBounce(self, x1, y1, x2, y2):
        overlappingObject = self.canvas.find_overlapping(
            x1,
            y1,
            x2,
            y2
        )

        for k in self.terrain.keys():
            if k in overlappingObject:
                if k == 1:
                    self.setFinished(True)
                    return True
                else:
                    self.setAlive(False)
                    return k
        return True

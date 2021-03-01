from Swarm import Swarm
from config import FishConstants, WindowConstants
from tkinter import TclError, Tk, Canvas


def generateTerrain(canvas):
    goal = canvas.create_rectangle(
        WindowConstants.goal_list,
        fill=WindowConstants.goal_color
    )
    terrain = {
        goal: WindowConstants.goal_list,
    }

    for obstacle in WindowConstants.obstacle_List.values():

        key = canvas.create_rectangle(
            obstacle,
            fill=WindowConstants.obstacle_color
        )
        terrain[key] = obstacle

    return terrain


root = Tk()
root.title("Fish")
root.resizable(False, False)

canvas = Canvas(root, height=WindowConstants.height,
                width=WindowConstants.width, 
                background=WindowConstants.background_color)

terrain = generateTerrain(canvas=canvas)

FISH_SWARM = Swarm(root=root, canvas=canvas, terrain=terrain)

deltaTime = 0

try:
    while True:
        FISH_SWARM.run()
except(TclError):
    pass

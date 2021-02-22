from Swarm import Swarm
from config import WindowConstants
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

GENERATION = 1

canvas = Canvas(root, height=WindowConstants.height,
                width=WindowConstants.width, 
                background=WindowConstants.background_color)

terrain = generateTerrain(canvas=canvas)

FISH_SWARM = Swarm(root=root, canvas=canvas, terrain=terrain)

try:
    while True:
        root.title(f"Fish Generation : {GENERATION}")

        FISH_SWARM.runSwarm()

        GENERATION += 1
except(TclError):
    pass

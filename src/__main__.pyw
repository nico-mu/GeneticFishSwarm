from tkinter.constants import END, NW, TOP
from Swarm import Swarm
from config import FishConstants, WindowConstants
from tkinter import BooleanVar, Button, Checkbutton, Entry, Frame, Label, Scrollbar, StringVar, TclError, Tk, Canvas, WRITABLE
from threading import Thread

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

def fillDNALabel():
    entry.configure(state="normal")
    entry.delete(0, END)
    entry.insert(0, FISH_SWARM.getBestDNA())
    entry.configure(state='readonly')

def run():
    try:
        while True:
            FISH_SWARM.run()
    except(TclError):
        pass

root = Tk()
root.title("Fish")
root.resizable(False, False)

canvas = Canvas(root, height=WindowConstants.height,
                width=WindowConstants.width, 
                background=WindowConstants.background_color)


terrain = generateTerrain(canvas=canvas)


frame = Frame(root)

doTrackLine = BooleanVar()
doTrackLine.set(False)
trackLineButton = Checkbutton(frame, text="Track Line", variable=doTrackLine)
trackLineButton.grid(row=0, column=0)

FISH_SWARM = Swarm(root=root, canvas=canvas, doTrackLine=doTrackLine, terrain=terrain)

showDNAButton = Button(frame, text="Show DNA", command=fillDNALabel)
showDNAButton.grid(row=0, column=1, sticky="ew")

entryVar = StringVar()
entry = Entry(frame, textvariable=entryVar, state='readonly', width=int(WindowConstants.width/10))
scroll = Scrollbar(frame, orient='horizontal', command=entry.xview)
entry.config(xscrollcommand=scroll.set)

frame.grid(row=1)
entry.grid(row=1, column=1, sticky='ew')
scroll.grid(row=2, column=1, sticky='ew')

deltaTime = 0

run()
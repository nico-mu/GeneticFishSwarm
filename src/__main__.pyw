from tkinter import (BooleanVar, Button, Canvas, Checkbutton, Entry, Frame,
                     Label, Scrollbar, Spinbox, StringVar, TclError, Tk)
from tkinter.constants import END

from typing_extensions import IntVar

from config import FishConstants, WindowConstants
from Swarm import Swarm


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
    bestDNAEntry.configure(state="normal")
    bestDNAEntry.delete(0, END)
    bestDNAEntry.insert(0, FISH_SWARM.getBestDNA())
    bestDNAEntry.configure(state='readonly')


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

numberOfFish = StringVar()
numberOfFish.set(str(FishConstants.number_of_fish))
fishCountLabel = Label(frame, text="Number of Fishes")
fishCountSpinBox = Spinbox(frame, textvariable=numberOfFish, from_=0, to=10000)

maxLifeSpan = StringVar()
maxLifeSpan.set(str(FishConstants.max_lifespan))
maxLifeSpanLabel = Label(frame, text="Number of Fish Lifecycles")
maxLifeSpanSpinBox = Spinbox(frame, textvariable=maxLifeSpan, from_=0, to=10000)

FISH_SWARM = Swarm(root=root, canvas=canvas,
                   doTrackLine=doTrackLine, terrain=terrain, numberOfFish=numberOfFish, maxLifeSpan=maxLifeSpan)

showDNAButton = Button(frame, text="Show DNA", command=fillDNALabel)
showDNAButton.grid(row=0, column=1, sticky="ew")

bestDNAEntryVar = StringVar()
bestDNAEntry = Entry(frame, textvariable=bestDNAEntryVar, state='readonly',
              width=int(WindowConstants.width/15))
scroll = Scrollbar(frame, orient='horizontal', command=bestDNAEntry.xview)
bestDNAEntry.config(xscrollcommand=scroll.set)

fishCountLabel.grid(row=0, column=2, sticky="ew")
fishCountSpinBox.grid(row=1, column=2, sticky="ew")

maxLifeSpanLabel.grid(row=0, column=3, sticky="ew")
maxLifeSpanSpinBox.grid(row=1, column=3, sticky="ew")

frame.grid(row=1)
bestDNAEntry.grid(row=1, column=1, sticky='ew')
scroll.grid(row=2, column=1, sticky='ew')

deltaTime = 0

run()

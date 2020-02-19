from PyQt5.QtWidgets import QLabel

from buttons import StartButton, HistoryCheckBox, StopButton, StepButton, ClearButton
from slider import FPSSlider


def createButtonsForGUI(canvas, knownPatternBox, controller):
    buttons = []
    start = StartButton(controller)
    historyCheckBox = HistoryCheckBox(canvas)
    buttons.append(start)
    buttons.append(StopButton(start.timer))
    buttons.append(StepButton(controller))
    buttons.append(ClearButton(controller))
    buttons.append(knownPatternBox)
    buttons.append(historyCheckBox)

    fpsSlider = FPSSlider(start)

    return fpsSlider, buttons


def generateLabelsForGUI():
    fpsLabel = QLabel('FPS:')
    fpsLabel.setFixedWidth(30)
    minLabel = QLabel('1')
    minLabel.setFixedWidth(10)

    return fpsLabel, minLabel

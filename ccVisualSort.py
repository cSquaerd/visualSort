import tkinter as tk
import tkinter.simpledialog as sdg
import tkinter.messagebox as mbx
import tkinter.font as tkf
import random as rnd
import time

base = tk.Tk()
base.title("Charlie Cook's Visual Sorting Demo")
base.resizable(False, False)

# Fonts
fontSmall = tkf.Font(family = "Consolas", size = 8)
fontNormal = tkf.Font(family = "Consolas", size = 10)
fontNormUnd = tkf.Font(family = "Consolas", size = 10, underline = 1)
fontNormBold = tkf.Font(family = "Consolas", size = 10, weight = "bold")
fontLarge = tkf.Font(family = "Consolas", size = 12)
fontLargeBold = tkf.Font(family = "Consolas", size = 12, weight = "bold")
fontSubtitle = tkf.Font(family = "Consolas", size = 12, slant = "italic")
fontTitle = tkf.Font(family = "Consolas", size = 12, weight = "bold", slant = "italic")
fontBigTitle = tkf.Font(family = "Consolas", size = 16, weight = "bold", slant = "italic")
fontName = tkf.Font(family = "Consolas", size = 16, weight = "bold")

frameControls = tk.LabelFrame(base, text = "Sorting Controls", bd = 4, relief = "raised", font = fontTitle)
frameControls.grid(row = 0, column = 0, padx = 4, pady = 4)

frameMain = tk.LabelFrame(base, text="Sorting Panel", bd = 4, relief = "raised", font = fontTitle)
frameMain.grid(row = 1, column = 0, padx = 4, pady = 4)


frameScreen = tk.Canvas(frameMain, width = 800, height = 400)
frameScreen.pack(padx = 4, pady = 4)

elementHeights = list(range(1, 11))
elementColorCoding = {"indicated": 0}

def processColor(element):
	colorNormal = "#2E52C4"
	colorIndicated = "#678DFF"
	#colorSwap = "#002080"
	return colorIndicated if element == elementColorCoding["indicated"] else colorNormal

def clearElements():
	for el in frameScreen.find_all():
		frameScreen.delete(el)

def updateElements(strNewElements):
	newElements = int(strNewElements)
	clearElements()

	global elementHeights

	if newElements == 0:
		newElements = elements.get()
	else:
		elementHeights = list(range(1, newElements + 1))

	elWidthUnit = round(800 / newElements, 2)
	elHeightUnit = round(400 / newElements, 2)

	for i in range(newElements):
		frameScreen.create_rectangle(elWidthUnit * i, 400, elWidthUnit * (i + 1), 400 - elHeightUnit * elementHeights[i], fill = processColor(i), width = 0)
		#fill = ("#678DFF" if ??? else "#2E52C4")

	frameScreen.update_idletasks()

elements = tk.IntVar()
scaleElements = tk.Scale(frameControls, label = "Sortable Elements", resolution = 10, from_ = 10, to = 400, length = 250, orient = "horizontal", variable = elements, command = updateElements, font = fontNormal)
scaleElements.grid(row = 0, column = 0, rowspan = 2, padx = 2, pady = 2)
updateElements(0)

sleepTime = tk.DoubleVar()
scaleSleep = tk.Scale(frameControls, label = "Time Delay on Swap (seconds)", resolution = 0.005, from_ = 0.005, to = 0.2, length = 250, orient = "horizontal", variable = sleepTime, font = fontNormal)
scaleSleep.grid(row = 0, column = 1, rowspan = 2, padx = 2, pady = 2)

def swap(elA, elB):
	elementHeights[elA] += elementHeights[elB]
	elementHeights[elB] -= elementHeights[elA]
	elementHeights[elB] *= -1
	elementHeights[elA] -= elementHeights[elB]
	updateElements(0)
	time.sleep(sleepTime.get())

def shuffleElements():
	rnd.shuffle(elementHeights)
	updateElements(0)

def bubbleSort():
	for i in range(elements.get() - 1):
		swaps = 0

		for j in range(elements.get() - i - 1):
			elementColorCoding["indicated"] = j
			if elementHeights[j] > elementHeights[j + 1]:
				swap(j, j + 1)
				swaps += 1

		if swaps == 0:
			break

def insertionSort():
	for i in range(1, elements.get()):
		j = i - 1
		while j >= 0 and elementHeights[j] > elementHeights[j + 1]:
			elementColorCoding["indicated"] = j
			swap(j + 1, j)
			j -= 1;

def selectionSort():
	def minIndex(firstIndex):
		min = firstIndex

		for i in range(firstIndex, elements.get()):
			if elementHeights[i] < elementHeights[min]:
				min = i

		return min

	for i in range(1, elements.get()):
		m = minIndex(i)

		while m >= i and elementHeights[m] < elementHeights[m - 1]:
			elementColorCoding["indicated"] = m
			swap(m, m - 1)
			m -= 1

buttonShuffle = tk.Button(frameControls, text = "Shuffle Elements", bd = 2, width = 16, command = shuffleElements, font = fontNormal)
buttonBubble = tk.Button(frameControls, text = "Bubble Sort", bd = 2, width = 16, command = bubbleSort, font = fontNormal)
buttonInsertion = tk.Button(frameControls, text = "Insertion Sort", bd = 2, width = 16, command = insertionSort, font = fontNormal)
buttonSelection = tk.Button(frameControls, text = "Selection Sort", bd = 2, width = 16, command = selectionSort, font = fontNormal)

buttonShuffle.grid(row = 0, column = 2, padx = 2, pady = 2)
buttonBubble.grid(row = 0, column = 3, padx = 2, pady = 2)
buttonInsertion.grid(row = 1, column = 2, padx = 2, pady = 2)
buttonSelection.grid(row = 1, column = 3, padx = 2, pady = 2)

base.mainloop()

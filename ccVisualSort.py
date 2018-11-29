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

elementHeights = list(range(1, 21))
elementColorCoding = {"indicated": 0, "sortedBorder": -1, "sortedSide": "none"}

def processColor(element):
	colorNormal = "#2E52C4"
	colorIndicated = "#678DFF"
	colorSorted = "#002080"
	return colorIndicated if element == elementColorCoding["indicated"] else \
		colorSorted if element <= elementColorCoding["sortedBorder"] and \
			elementColorCoding["sortedSide"] == "left" or \
		element >= elementColorCoding["sortedBorder"] and \
			elementColorCoding["sortedSide"] == "right" \
		else colorNormal

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
scaleElements = tk.Scale(frameControls, label = "Sortable Elements", resolution = 20, from_ = 20, to = 800, length = 250, orient = "horizontal", variable = elements, command = updateElements, font = fontNormal)
scaleElements.grid(row = 0, column = 0, rowspan = 2, padx = 2, pady = 2)
updateElements(0)

sleepTime = tk.DoubleVar()
sleepTimeFine = tk.DoubleVar()
scaleSleep = tk.Scale(frameControls, label = "Time Delay on Swap (seconds)", resolution = 0.005, from_ = 0, to = 0.2, length = 250, orient = "horizontal", variable = sleepTime, font = fontNormal)
scaleSleepFine = tk.Scale(frameControls, label = "Fine Time Delay on Swap (ms)", resolution = 0.1, from_ = 0, to = 4.9, length = 250, orient = "horizontal", variable = sleepTimeFine, font = fontNormal)
scaleSleep.grid(row = 2, column = 0, rowspan = 2, padx = 2, pady = 2)
scaleSleepFine.grid(row = 4, column = 0, rowspan = 2, padx = 2, pady = 2)

def swap(elA, elB):
	if elA == elB:
		return None

	elementHeights[elA] += elementHeights[elB]
	elementHeights[elB] -= elementHeights[elA]
	elementHeights[elB] *= -1
	elementHeights[elA] -= elementHeights[elB]
	updateElements(0)
	time.sleep(sleepTime.get() + sleepTimeFine.get() / 1000)

def shuffleElements():
	rnd.shuffle(elementHeights)
	elementColorCoding["indicated"] = 0
	elementColorCoding["sortedBorder"] = -1
	elementColorCoding["sortedSide"] = "none"
	updateElements(0)

def bubbleSort():
	elementColorCoding["sortedSide"] = "right"
	for i in range(elements.get() - 1):
		swaps = 0

		for j in range(elements.get() - i - 1):
			elementColorCoding["indicated"] = j + 1
			if elementHeights[j] > elementHeights[j + 1]:
				swap(j, j + 1)
				swaps += 1

		elementColorCoding["sortedBorder"] = j

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
			elementColorCoding["indicated"] = m - 1
			swap(m, m - 1)
			m -= 1

def merge(baseLeft, lengthLeft, baseRight, lengthRight):
	localArray = elementHeights[baseLeft : baseLeft + lengthLeft + lengthRight]
	localLeft = 0
	localRight = lengthLeft

	for k in range(baseLeft, baseLeft + lengthLeft + lengthRight):
		elementColorCoding["indicated"] = k

		if localRight == lengthLeft + lengthRight or (localLeft < lengthLeft and localArray[localLeft] < localArray[localRight]):
			elementHeights[k] = localArray[localLeft]
			localLeft += 1
		else:
			elementHeights[k] = localArray[localRight]
			localRight += 1

		updateElements(0)
		time.sleep(sleepTime.get() + sleepTimeFine.get() / 1000)

def mergeSort(base, length):
	if length > 1:
		lengthLeft = length // 2
		lengthRight = length - lengthLeft
		baseLeft = base
		baseRight = base + lengthLeft

		mergeSort(baseLeft, lengthLeft)
		mergeSort(baseRight, lengthRight)

		merge(baseLeft, lengthLeft, baseRight, lengthRight)

#TODO: Quick & Bogo Sort.

def heapify(head, heapSize):
	left = 2 * head + 1
	right = 2 * head + 2
	largest = head

	if (left < heapSize and elementHeights[left] > elementHeights[head]):
		largest = left
	if (right < heapSize and elementHeights[right] > elementHeights[largest]):
		largest = right
	if largest != head:
		elementColorCoding["indicated"] = head
		swap(largest, head)

def buildHeap(length):
	for i in range(length // 2, -1, -1):
		heapify(i, length)

def heapSort():
	buildHeap(elements.get())

	for i in range(elements.get() - 1, 0, -1):
		swap(0, i)
		buildHeap(i)

def bogoSort():
	if elements.get() > 10:
		mbx.showwarning("Warning!", "Bogo Sort's time complextity is n-factorial. It cannot in good faith be run on a list larger than 10 elements.")
		return None
	else:
		mbx.showinfo("Notice", "Only the fine time delay will be used in this sorting run.")

	sorted = False
	while not sorted:
		rnd.shuffle(elementHeights)
		updateElements(0)
		time.sleep(sleepTimeFine.get() / 1000)

		broke = False
		for i in range(elements.get() - 1):
			if elementHeights[i] > elementHeights[i + 1]:
				broke = True
				break

		if not broke:
			sorted = True

def qsPartition(left, right):
	elementColorCoding["indicated"] = right
	pivot=elementHeights[right]
	i = left

	for j in range(left, right):
		if elementHeights[j] < pivot:
			if i != j:
				swap(i, j)

			i += 1

	swap(i, right)
	return i

def quickSort(left, right):
    if left < right:
        pivot = qsPartition(left, right)
        quickSort(left, pivot - 1)
        quickSort(pivot + 1, right)

buttonShuffle = tk.Button(frameControls, text = "Shuffle Elements", bd = 2, width = 16, command = shuffleElements, font = fontNormal)
buttonBubble = tk.Button(frameControls, text = "Bubble Sort", bd = 2, width = 16, command = bubbleSort, font = fontNormal)
buttonInsertion = tk.Button(frameControls, text = "Insertion Sort", bd = 2, width = 16, command = insertionSort, font = fontNormal)
buttonSelection = tk.Button(frameControls, text = "Selection Sort", bd = 2, width = 16, command = selectionSort, font = fontNormal)
buttonMerge = tk.Button(frameControls, text = "Merge Sort", bd = 2, width = 16, command = lambda: mergeSort(0, elements.get()), font = fontNormal)
buttonHeap = tk.Button(frameControls, text = "Heap Sort", bd = 2, width = 16, command = heapSort, font = fontNormal)
buttonQuick = tk.Button(frameControls, text = "Quick Sort", bd = 2, width = 16, command = lambda: quickSort(0, elements.get() - 1), font = fontNormal)
buttonBogo = tk.Button(frameControls, text = "Bogo Sort", bd = 2, width = 16, command = bogoSort, font = fontNormal)

buttonShuffle.grid(row = 0, column = 1, padx = 2, pady = 2)
buttonBubble.grid(row = 1, column = 1, padx = 2, pady = 2)
buttonInsertion.grid(row = 2, column = 1, padx = 2, pady = 2)
buttonSelection.grid(row = 3, column = 1, padx = 2, pady = 2)
buttonMerge.grid(row = 4, column = 1, padx = 2, pady = 2)
buttonHeap.grid(row = 5, column = 1, padx = 2, pady = 2)
buttonQuick.grid(row = 6, column = 1, padx = 2, pady = 2)
buttonBogo.grid(row = 7, column = 1, padx = 2, pady = 2)

base.mainloop()

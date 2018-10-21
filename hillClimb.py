# python3
#
# Searches for highest point on 2D gaussian function
#
# adapted from gisikw:
# https://gist.github.com/gisikw/f093e8cfcdd4f082672430974f785dbc

import math, copy

def main():
	findPeak()

def findPeak():
	point = [0, 0]
	solution = improveConverge(point)
	print(solution)

def getScore(samplePoint):
	score = 1000*math.exp(-(((samplePoint[0] + 14.237)**2/(2*10**2)) + ((samplePoint[1] - 20.216)**2/(2*10**2))))
	return score

def improveConverge(data):
	for stepSize in [10, 1, 0.1, 0.01, 0.001]:
		Finished = False
		while Finished == False:
			oldScore = getScore(data)
			data = improve(data, stepSize)
			if oldScore >= getScore(data):
				Finished = True
	return data

def improve(data, stepSize):
	bestCandidate = data
	highestScore = getScore(data)
	candidates = []
	index = 0
	while index <= len(data) - 1:
		incCandidate = copy.deepcopy(data)
		decCandidate = copy.deepcopy(data)
		incCandidate[index] += stepSize
		candidates.append(incCandidate)
		decCandidate[index] -= stepSize
		candidates.append(decCandidate)
		index += 1
	for candidate in candidates:
		candidateScore = getScore(candidate)
		if candidateScore > highestScore:
			highestScore = candidateScore
			bestCandidate = candidate
	return bestCandidate

main()
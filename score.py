#!/bin/python

import sys

photos = []

def parseLine(line):
    global photos
    sp = line.split(' ')
    photos.append(set(sp[2:]))

def readPhotos(path):
    global photos
    with open(path) as f:
        lines = f.readlines()
        noPhotos = int(lines[0])
        for l in lines[1:]:
            parseLine(l.rstrip())

def calcScore(photoFile, slides):
    global photos
    readPhotos(photoFile)
    score = 0
    with open(slides, 'r') as f:
        lines = f.readlines()
        prevTags = set()
        for l in lines[1:]:
            sp = l.split(' ')
            currentTags = set()
            if len(sp) == 2:
                #vert
                currentTags = photos[int(sp[0])].union(photos[int(sp[1])])
            else:
                #horizontal
                currentTags = photos[int(sp[0])]
            #calc score
            if prevTags != set():
                leftSize = len(prevTags.difference(currentTags))
                midSize = len(prevTags.union(currentTags))
                rightSize = len(currentTags.difference(prevTags))
                score += min(min(leftSize, midSize), rightSize)
            prevTags = currentTags
    return score

print(calcScore(str(sys.argv[1]), str(sys.argv[2])))

"""
A Python script to crop the audio file into each number following the 24-number
transcription
Author: CS398: Independent Study: Computational Linguistic Spring 2022 classmate
Instructor: Professor Nanette 
"""

from scipy.io import wavfile
from GenTimestamp import timeStampDict
import math

audioFileName = input("Please input the wav audio file name: ")
rate, data = wavfile.read(audioFileName)
audioFileName_root = audioFileName[0:6]

for word in timeStampDict:
    minAtFrame = math.floor(rate * timeStampDict[word][0])
    maxAtFrame = math.ceil(rate * timeStampDict[word][1])
    splitAudio = data[minAtFrame:maxAtFrame]
    # Changing the naming convention appropriately. The idea is exactly the
    # same. Read the wav file and choping the audio based on the dictionary
    # result from the GenTimestamp module.
    finalNaming = audioFileName_root + "W" + str(word) + ".wav"
    wavfile.write(finalNaming, rate, splitAudio)




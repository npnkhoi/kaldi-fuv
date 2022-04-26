"""
A Python script to crop the audio file into each word following the 24-number
transcription
Author: CS398: Independent Study: Computational Linguistic Spring 2022 classmate
Instructor: Professor Nanette 
"""

from scipy.io import wavfile # Use this package to read and write the wav file
# Use the following package to get the data analysis from the textgrid
import math
import os
import wavio as wv
import textgrid # textgrid is a useful module to read the textgrid file type

def gen_timestamp(number):
    try:
        filename =  number + '.TextGrid'
        tg = textgrid.TextGrid.fromFile(filename)
    except:
        filename =  number + '.textgrid'
        tg = textgrid.TextGrid.fromFile(filename)

    SILENCE = "sil"
    LAST_CHARACTER_FILENAME = -10

    # Encoding the order of the word of the transcript appropriately. We would check
    # the last character of the file name to determine which part of the transcript
    # we currently are. Thus, the index to find the last character of the file name
    # is -10 (started from the back). These encoding numbers are based on the helper
    # spreadsheet accompany to.
    encoding = 1
    if filename[LAST_CHARACTER_FILENAME] == '1':
        encoding = 1
    elif filename[LAST_CHARACTER_FILENAME] == '2':
        encoding = 18
    elif filename[LAST_CHARACTER_FILENAME] == '3':
        encoding = 38
    elif filename[LAST_CHARACTER_FILENAME] == '4':
        encoding = 57
    elif filename[LAST_CHARACTER_FILENAME] == '5':
        encoding = 75
    elif filename[LAST_CHARACTER_FILENAME] == '6':
        encoding = 95
    i = 0 # Start of the interval (the first interval to go through)

    # Key: id of the number
    # Value: list of two elements: [time_min, time_max]
    timeStampDict = {} # Final data will be recorded as a dictionary

    while(True):
        try:
            # Access the current interval
            current_interval = tg[0][i]
            # Simply approach: Eliminate all of the sil intervals. Assign the rest
            # of the word transcipt into an encoding code with start and end
            # intevral can be extracted from the interval class.
            if(current_interval.mark != SILENCE):
                start = current_interval.minTime 
                end = current_interval.maxTime
                timeStampDict[encoding] = [start, end]
                encoding += 1
            i += 1
        except IndexError:
            break

    return timeStampDict


def split_audio_word_and_save(save_folder_path, file_path):
    # Prompt the user to input the filename as well as read the wav file into Python
    audioFileName = file_path + ".wav"
    rate, data = wavfile.read(audioFileName, 'r')
    # Take the container folder name
    audioFileName_root = audioFileName.split('/')[-2]

    timeStampDict = gen_timestamp(file_path)

    for word in timeStampDict:
        # This is totally based on the formula that we have looked up online.
        minAtFrame = math.floor(rate * timeStampDict[word][0])
        maxAtFrame = math.ceil(rate * timeStampDict[word][1])
        splitAudio = data[minAtFrame:maxAtFrame]
        # Rename the sequential audio files to match with the naming convention of
        # the dataset
        finalNaming = f"{audioFileName_root}_W{str(word).zfill(2)}.wav"
        save_path = os.path.join(save_folder_path, finalNaming)
        wavfile.write(save_path, rate, splitAudio)   
        print('Save file at', save_path) 




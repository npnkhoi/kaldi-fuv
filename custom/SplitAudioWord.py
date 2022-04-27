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

id_to_filename = {1: 'mootj_1', 2: 'trawm_1', 3: 'tams_1', 4: 'muowi_1', 5: 'hai_1'
                  , 6: 'saus_1', 7: 'trawm_2', 8: 'ler_1', 9: 'saus_2', 10: 'mootj_2'
                  , 11: 'trawm_3', 12: 'ba_1', 13: 'muowi_2', 14: 'tams_2', 15: 'bayr_1'
                  , 16: 'muowi_3', 17: 'hai_2', 18: 'tams_3', 19: 'trawm_4', 20: 'tams_4'
                  , 21: 'muowi_4', 22: 'ba_2', 23: 'chins_1', 24: 'trawm_5', 25: 'tams_5'
                  , 26: 'muowi_5', 27: 'saus_3', 28: 'mootj_3', 29: 'trawm_6', 30: 'ba_3'
                  , 31: 'muowi_6', 32: 'saus_4', 33: 'bayr_2', 34: 'trawm_7', 35: 'bayr_3'
                  , 36: 'muowi_7', 37: 'ba_4', 38: 'mootj_4', 39: 'trawm_8', 40: 'chins_2'
                  , 41: 'lawm_1', 42: 'chins_3', 43: 'trawm_9', 44: 'bayr_4', 45: 'muowi_8'
                  , 46: 'saus_5', 47: 'nawm_1', 48: 'trawm_10', 49: 'saus_6', 50: 'muowi_9'
                  , 51: 'ba_5', 52: 'hai_3', 53: 'trawm_11', 54: 'boons_1', 55: 'muowi_10'
                  , 56: 'bayr_5', 57: 'saus_7', 58: 'trawm_12', 59: 'tams_6', 60: 'muowi_11'
                  , 61: 'ba_6', 62: 'nawm_2', 63: 'trawm_13', 64: 'muowif_1', 65: 'saus_8'
                  , 66: 'trawm_14', 67: 'chins_4', 68: 'muowi_12', 69: 'moots_1', 70: 'mootj_5'
                  , 71: 'trawm_15', 72: 'hai_4', 73: 'muowi_13', 74: 'bayr_6', 75: 'tams_7'
                  , 76: 'trawm_16', 77: 'tams_8', 78: 'muowi_14', 79: 'hai_5', 80: 'mootj_6'
                  , 81: 'trawm_17', 82: 'saus_9', 83: 'muowi_15', 84: 'bayr_7', 85: 'ba_7'
                  , 86: 'trawm_18', 87: 'hai_6', 88: 'muowi_16', 89: 'hai_7', 90: 'boons_2'
                  , 91: 'trawm_19', 92: 'ba_8', 93: 'muowi_17', 94: 'hai_8', 95: 'ba_9'
                  , 96: 'muowi_18', 97: 'ba_10', 98: 'hai_9', 99: 'trawm_20', 100: 'saus_10'
                  , 101: 'muowi_19', 102: 'ba_11', 103: 'hai_10', 104: 'trawm_21', 105: 'nawm_3'
                  , 106: 'muowi_20', 107: 'bayr_8', 108: 'trawm_22', 109: 'bayr_9', 110: 'muowi_21'
                  , 111: 'saus_11'}

def gen_timestamp(number):
    try:
        filename =  number + '.TextGrid'
        tg = textgrid.TextGrid.fromFile(filename)
    except:
        filename =  number + '.textgrid'
        tg = textgrid.TextGrid.fromFile(filename)

    SILENCE = ["sil", "silent", "silence"]
    LAST_CHARACTER_FILENAME = -10

    # Encoding the order of the word of the transcript appropriately. We would check
    # the last character of the file name to determine which part of the transcript
    # we currently are. Thus, the index to find the last character of the file name
    # is -10 (started from the back). These encoding numbers are based on the helper
    # spreadsheet accompany to.
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
            current_annotation = current_interval.mark
            current_annotation = current_annotation.lower()
            # Simply approach: Eliminate all of the sil intervals. Assign the rest
            # of the word transcipt into an encoding code with start and end
            # intevral can be extracted from the interval class.
            if(current_annotation not in SILENCE):
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
        finalNaming = audioFileName_root + "_W" + id_to_flename[word] + ".wav"
        save_path = os.path.join(save_folder_path, finalNaming)
        wavfile.write(save_path, rate, splitAudio)   
        print('Save file at', save_path) 




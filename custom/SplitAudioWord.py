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
import pandas as pd

csvKeepTrackName = "TranscriptToName.csv"
KeepTrackData = pd.read_csv(csvKeepTrackName)

id_to_filename = {1: 'mootj_01', 2: 'trawm_01', 3: 'tams_01', 4: 'muowi_01', 5: 'hai_01'
              , 6: 'saus_01', 7: 'trawm_02', 8: 'ler_01', 9: 'saus_02', 10: 'mootj_02'
              , 11: 'trawm_03', 12: 'ba_01', 13: 'muowi_02', 14: 'tams_02', 15: 'bayr_01'
              , 16: 'muowi_03', 17: 'hai_02', 18: 'tams_03', 19: 'trawm_04', 20: 'tams_04'
              , 21: 'muowi_04', 22: 'ba_02', 23: 'chins_01', 24: 'trawm_05', 25: 'tams_05'
              , 26: 'muowi_05', 27: 'saus_03', 28: 'mootj_03', 29: 'trawm_06', 30: 'ba_03'
              , 31: 'muowi_06', 32: 'saus_04', 33: 'bayr_02', 34: 'trawm_07', 35: 'bayr_03'
              , 36: 'muowi_07', 37: 'ba_04', 38: 'mootj_04', 39: 'trawm_08', 40: 'chins_02'
              , 41: 'lawm_01', 42: 'chins_03', 43: 'trawm_09', 44: 'bayr_04', 45: 'muowi_08'
              , 46: 'saus_05', 47: 'nawm_01', 48: 'trawm_10', 49: 'saus_06', 50: 'muowi_09'
              , 51: 'ba_05', 52: 'hai_03', 53: 'trawm_11', 54: 'boons_01', 55: 'muowi_10'
              , 56: 'bayr_05', 57: 'saus_07', 58: 'trawm_12', 59: 'tams_06', 60: 'muowi_11'
              , 61: 'ba_06', 62: 'nawm_02', 63: 'trawm_13', 64: 'muowif_01', 65: 'saus_08'
              , 66: 'trawm_14', 67: 'chins_04', 68: 'muowi_12', 69: 'moots_01', 70: 'mootj_05'
              , 71: 'trawm_15', 72: 'hai_04', 73: 'muowi_13', 74: 'bayr_06', 75: 'tams_07'
              , 76: 'trawm_16', 77: 'tams_08', 78: 'muowi_14', 79: 'hai_05', 80: 'mootj_06'
              , 81: 'trawm_17', 82: 'saus_09', 83: 'muowi_15', 84: 'bayr_07', 85: 'ba_07'
              , 86: 'trawm_18', 87: 'hai_06', 88: 'muowi_16', 89: 'hai_07', 90: 'boons_02'
              , 91: 'trawm_19', 92: 'ba_08', 93: 'muowi_17', 94: 'hai_08', 95: 'ba_09'
              , 96: 'muowi_18', 97: 'ba_10', 98: 'hai_09', 99: 'trawm_20', 100: 'saus_10'
              , 101: 'muowi_19', 102: 'ba_11', 103: 'hai_10', 104: 'trawm_21', 105: 'nawm_03'
              , 106: 'muowi_20', 107: 'bayr_08', 108: 'trawm_22', 109: 'bayr_09', 110: 'muowi_21'
              , 111: 'saus_11'}

word_to_telex = {}
for i in range(len(KeepTrackData)):
    current_transcript = KeepTrackData.script[i]
    current_telex = KeepTrackData.filename[i]
    word_to_telex[current_transcript] = current_telex

word_frequency = {}
for i in range(len(KeepTrackData)):
    current_telex = KeepTrackData.filename[i]
    word_frequency[current_telex] = 0

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
            current_annotation = current_annotation.strip()
            current_annotation = current_annotation.lower()
            # Simply approach: Eliminate all of the sil intervals. Assign the rest
            # of the word transcipt into an encoding code with start and end
            # intevral can be extracted from the interval class.
            if(current_annotation not in SILENCE):
                start = current_interval.minTime 
                end = current_interval.maxTime
                telex_match = word_to_telex[current_annotation]
                word_frequency[telex_match] = word_frequency[telex_match] + 1
                saveName = telex_match + "_" + str(word_frequency[telex_match])
                timeStampDict[saveName] = [start, end]
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
    audioFileName_root = audioFileName.split('\\')[-2]

    timeStampDict = gen_timestamp(file_path)

    for word in timeStampDict:
        # This is totally based on the formula that we have looked up online.
        minAtFrame = math.floor(rate * timeStampDict[word][0])
        maxAtFrame = math.ceil(rate * timeStampDict[word][1])
        splitAudio = data[minAtFrame:maxAtFrame]
        # Rename the sequential audio files to match with the naming convention of
        # the dataset
        finalNaming = audioFileName_root + "_W_" + word + ".wav"
        save_path = os.path.join(save_folder_path, finalNaming)
        wavfile.write(save_path, rate, splitAudio)   
        print('Save file at', save_path) 

print



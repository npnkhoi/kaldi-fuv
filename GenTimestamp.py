"""
A Python script to generate all of the necessary start and end timestamps of all
numbers in the number transcription
Author: CS398: Independent Study: Computational Linguistic Spring 2022 classmate
Instructor: Professor Nanette 
"""

import textgrid

filename = input("Please input the filename (as a TextGrid file): ")
tg = textgrid.TextGrid.fromFile(filename)

# Because we have problems when comparing Vietnamese string by another txt file,
# we have decided to include the transcription manually there for the precise
# comparison.
transcript24nums = [["một trăm tám mươi hai", "sáu trăm lẻ sáu", "một trăm ba mươi tám", "bảy mươi hai"],
                    ["tám trăm tám mươi ba", "chín trăm tám mươi sáu", "một trăm ba mươi sáu", "bảy trăm bảy mươi ba"],
                    ["một trăm chín lăm", "chín trăm bảy mươi sáu", "năm trăm sáu mươi ba", "hai trăm bốn mươi bảy"],
                    ["sáu trăm tám mươi ba", "năm trăm mười", "sáu trăm chín mươi mốt", "một trăm hai mươi bảy"],
                    ["tám trăm tám mươi hai", "một trăm sáu mươi bảy", "ba trăm hai mươi hai", "bốn trăm ba mươi hai"],
                    ["ba mươi ba", "hai trăm sáu mươi ba", "hai trăm năm mươi", "bảy trăm bảy mươi sáu"]]
# This will depend on what file we are currently looking at.
transcriptOneFile = []

SILENCE = "sil"
LAST_CHARACTER_FILENAME = -10

# Similar to the previous GenTimestamp script for word, we would need to convert
# each number into an id for the naming convention later. In addition, we would
# also need to select the appropriate sub-transcript depending on the specific
# file we are at.
encoding = 1
fileTxtName = ""
if filename[LAST_CHARACTER_FILENAME] == '1':
    encoding = 1
    transcriptOneFile = transcript24nums[0]
elif filename[LAST_CHARACTER_FILENAME] == '2':
    encoding = 5
    transcriptOneFile = transcript24nums[1]
elif filename[LAST_CHARACTER_FILENAME] == '3':
    encoding = 9
    transcriptOneFile = transcript24nums[2]
elif filename[LAST_CHARACTER_FILENAME] == '4':
    encoding = 13
    transcriptOneFile = transcript24nums[3]
elif filename[LAST_CHARACTER_FILENAME] == '5':
    encoding = 17
    transcriptOneFile = transcript24nums[4]
elif filename[LAST_CHARACTER_FILENAME] == '6':
    encoding = 21
    transcriptOneFile = transcript24nums[5]

    
index = 0 # Start of the interval

# Key: id of the number
# Value: list of two elements: [time_min, time_max]
timeStampDict = {} # Final data will be recorded as a dictionary
j = 0
# Traverse to all of the numbers in a file
for k in range(len(transcriptOneFile)):
    i = 0
    correct = True
    numberList = transcriptOneFile[k].split()
    
    # Match each character with each other to see any errors from the annotaters
    while(i < len(numberList)):
        try:
            current_interval = tg[0][j]
            # Skip that interval if the interval is silent interval
            if(current_interval.mark == SILENCE):
                j += 1
            else:
                if(numberList[i] == current_interval.mark):
                    # Start word of the number
                    if i == 0:
                        start = current_interval.minTime
                    # End word of the number
                    if i == len(numberList) - 1:
                        end = current_interval.maxTime
                    # Moving to the next word
                    i += 1
                    j += 1

                # Wrong case: In this case, mark the flag as false and announce
                # the message to the user, then exit the script.        
                else:
                    correct = False
                    print("This file " + filename + " is error")
                    exit()
                
        except IndexError:
            break
    
    # Mark the result to the dictionary to prepare for the splitting portion.
    timeStampDict[encoding] = [start, end]
    encoding += 1


    

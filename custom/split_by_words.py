"""
This script splits the audio in the source folder, put them
in a destination folder, along with the data files (text, 
wav.scp, spk2utt).

The source folder is downloaded and modified from ASR Google Drive
in the afternoon of April 27, 2022.

Author: Khoi
"""
import math
import os
import subprocess
from scipy.io import wavfile

from custom.split_utils import VN2TELEX, get_words_from_textgrid

SRC_FOLDER = 'Data-May10' # source folder
AUDIO_FOLDER = 'numbers_audio'
TRAIN_FOLDER = os.path.join('data', 'train')
TEST_FOLDER = os.path.join('data', 'test')
ALL_SUBJECTS = ['S_S01', 'S_S03', 'S_S05', 'S_S07', 'S_S01', 'S_S17']
TRAIN_SUBJECTS = ALL_SUBJECTS[:-len(ALL_SUBJECTS) // 5 + 1] # split train:test 80:20

# Create folders
subprocess.run(['rm', '-r', AUDIO_FOLDER])
subprocess.run(['mkdir', '-p', AUDIO_FOLDER])
subprocess.run(['mkdir', '-p', TRAIN_FOLDER])
subprocess.run(['mkdir', '-p', TEST_FOLDER])

# Reset files
for folder in [TRAIN_FOLDER, TEST_FOLDER]:
  for filename in ['utt2spk', 'text', 'wav.scp']:
    subprocess.run(['rm', os.path.join(folder, filename)])

spk2utt = {}
count_success = 0

# Browse all textgrid files
for path, subdirs, files in os.walk(SRC_FOLDER):
  for name in sorted(files):
    if name[-8:].lower() != 'textgrid':
      continue
    
    # Read audio and textgrid
    label = name[:-9]
    words = get_words_from_textgrid(os.path.join(path, name))
    rate, wav_data = wavfile.read(os.path.join(path, label + '.wav'))
    num_words = len(words)

    # Browse all words
    for i in range(num_words):
      interval = words[i]
      text = interval[2]

      # spk2utt
      tokens = label.split('_')
      speaker = tokens[0] + '_' + tokens[1]
      spk2utt.setdefault(speaker, {
        'utt': [],
        'cnt': {}
      })
      try:
        encoded_text = VN2TELEX[text.strip()]
      except:
        print(f'WARNING: Skipping unrecognized word "{text}" in {label}')
        continue

      spk2utt[speaker]['cnt'].setdefault(encoded_text, 0)
      spk2utt[speaker]['cnt'][encoded_text] += 1
      new_label = f"{speaker}_{encoded_text}_{str(spk2utt[speaker]['cnt'][encoded_text]).rjust(2, '0')}"
      spk2utt[speaker]['utt'].append(new_label)

      # save .wav (split)
      minAtFrame = math.floor(rate * interval[0])
      maxAtFrame = math.ceil(rate * interval[1])
      splitAudio = wav_data[minAtFrame:maxAtFrame]
      dest_filename = os.path.join(AUDIO_FOLDER, f'{new_label}.wav')
      wavfile.write(dest_filename, rate, splitAudio)
      # print(interval[2], dest_filename)

      # save text
      folder = TRAIN_FOLDER if speaker in TRAIN_SUBJECTS else TEST_FOLDER
      with open(os.path.join(folder, 'text'), 'a') as f:
        f.write(f'{new_label} {interval[2]}\n')

      # save wav.scp
      with open(os.path.join(folder, 'wav.scp'), 'a') as f:
        f.write(f'{new_label} {dest_filename}\n')
      
      count_success += 1      

print(f'Successfullly split {count_success} audio files.')
# write spk2utt
for speaker, value in sorted(spk2utt.items()):
  folder = TRAIN_FOLDER if speaker in TRAIN_SUBJECTS else TEST_FOLDER
  with open(os.path.join(folder, 'utt2spk'), 'a') as f:
    for audio in value['utt']:
      f.write(f'{audio} {speaker}\n')

# sort the lines in data files
for folder in [TRAIN_FOLDER, TEST_FOLDER]:
  for filename in ['utt2spk', 'text', 'wav.scp']:
    with open(os.path.join(folder, filename), 'r') as f:
      lines = f.readlines()
    lines.sort()
    with open(os.path.join(folder, filename), 'w+') as f:
      f.writelines(lines)
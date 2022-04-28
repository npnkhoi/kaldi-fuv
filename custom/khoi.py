import math
import os
import subprocess
from matplotlib.pyplot import text
from scipy.io import wavfile

from custom.kutils import get_words_from_textgrid

src_folder = 'Data_Apr27'
dest_folder = 'khoi_data'
train_subjects = ['S_S01', 'S_S04', 'S_S05', 'S_S08', 'S_S13', 'S_S18', 'S_S19', 'S_S03',  'S_S06', 'S_S09', 'S_S17']

subprocess.run(['rm', '-r', dest_folder])
subprocess.run(['mkdir', '-p', os.path.join(dest_folder, 'audio')])
subprocess.run(['mkdir', '-p', os.path.join(dest_folder, 'train')])
subprocess.run(['mkdir', '-p', os.path.join(dest_folder, 'test')])

spk2utt = {}

for path, subdirs, files in os.walk(src_folder):
  for name in files:
    if name[-8:].lower() != 'textgrid':
      continue
    print(os.path.join(path, name))

    label = name[:-9]
    
    words = get_words_from_textgrid(os.path.join(path, name))
    rate, wav_data = wavfile.read(os.path.join(path, label + '.wav'))

    num_words = len(words)

    for i in range(num_words):
      interval = words[i]
      minAtFrame = math.floor(rate * interval[0])
      maxAtFrame = math.ceil(rate * interval[1])
      splitAudio = wav_data[minAtFrame:maxAtFrame]
      new_label = f'{label}_{i}'
      dest_filename = os.path.join(dest_folder, 'audio', f'{new_label}.wav')
      wavfile.write(dest_filename, rate, splitAudio)
      print(interval[2], dest_filename)

      tokens = new_label.split('_')
      speaker = tokens[0] + '_' + tokens[1]
      spk2utt.setdefault(speaker, [])
      spk2utt[speaker].append(new_label)

      split = 'train' if speaker in train_subjects else 'test'
      with open(os.path.join(dest_folder, split, 'text'), 'a') as f:
        f.write(f'{new_label} {interval[2]}\n')

      with open(os.path.join(dest_folder, split, 'wav.scp'), 'a') as f:
        f.write(f'{new_label} {dest_filename}\n')
      

for speaker, value in spk2utt.items():
  split = 'train' if speaker in train_subjects else 'test'
  with open(os.path.join(dest_folder, split, 'spk2utt'), 'a') as f:
    f.write(f'{speaker} ')
    for audio in value:
      f.write(f'{audio} ')
    f.write('\n')
from custom.utils import split_subject

src_folder = 'numbers_audio/train/'
dest_folder = 'numbers/audio/'
subjects = ['S_S01', 'S_S04', 'S_S05', 'S_S08', 'S_S13', 'S_S18', 'S_S19', 'S_S03',  'S_S06', 'S_S09', 'S_S17']

for subject in subjects:
  split_subject(src_folder, dest_folder, subject)
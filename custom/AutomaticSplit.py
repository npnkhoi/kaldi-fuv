import SplitAudioWord
import os

root_path = "/home/cs398/kaldi/egs/numbers/numbers_audio/train"
save_folder_path = "/home/cs398/kaldi/egs/numbers/data_word/word_audio/train"
folder_names = ['S_S01', 'S_S04', 'S_S05', 'S_S08', 'S_S13', 'S_S18', 'S_S19', 'S_S03',  'S_S06', 'S_S09', 'S_S17']

for folder in folder_names:
    for i in range(1,7):
        filename = f'{folder}_D{str(i).zfill(1)}'
        file_path = os.path.join(root_path, folder, filename)
        save_folder = os.path.join(save_folder_path, folder)
        SplitAudioWord.split_audio_word_and_save(save_folder, file_path)

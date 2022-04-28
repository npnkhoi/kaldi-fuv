import SplitAudioWord
import os

root_path = "C:\\Users\\Thuan\\Documents\\GitHub\\kaldi-fuv\\custom"
save_folder_path = "C:\\Users\\Thuan\\Documents\\GitHub\\kaldi-fuv\\custom\\Audio"
folder_names = ['S_S05']

for folder in folder_names:
    for i in range(1,7):
        filename = f'{folder}_D{str(i).zfill(1)}'
        file_path = os.path.join(root_path, folder, filename)
        save_folder = os.path.join(save_folder_path, folder)
        SplitAudioWord.split_audio_word_and_save(save_folder, file_path)

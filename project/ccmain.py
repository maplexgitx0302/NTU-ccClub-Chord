import os, re, csv
import subprocess
import numpy as np
import pandas as pd
import librosa
import soundfile
import sounddevice as sd
import torch
from torch.utils.data import Dataset
import matplotlib.pyplot as plt
import ccpreprocess, ccdownload, ccwebcrawl, ccchord, ccplay

np.random.seed(0)
torch.manual_seed(0)

dir_path   = os.path.abspath('')
npy_path   = os.path.join(dir_path, "music_numpydata")
excel_path = os.path.join(dir_path, 'ccClub music data (popular music).xlsx')
excel_data = pd.read_excel(excel_path, dtype={'Capo':int, '3 or 4':int})

cutdown_path = os.path.join(dir_path, 'music_cutdown')
if os.path.isdir(cutdown_path) == False:
    os.mkdir(cutdown_path)

for i in range(len(excel_data)):
    ccdownload.yt_wav(link=excel_data['Link'][i], file_name=excel_data['Title'][i])
    original_music = os.path.join(ccdownload.music_path, f"{excel_data['Title'][i]}.wav")
    cutdown_music  = os.path.join(cutdown_path, f"{excel_data['Title'][i]}.wav")
    print(f"Now cutting down {excel_data['Title'][i]} ... ", end='')
    if os.path.isfile(cutdown_music) == False:
        y, sr = librosa.load(original_music)
        cutdown_start = int(sr * excel_data['Start_Second'][i])
        cutdown_len   = int(len(excel_data['Chords'][i].strip('|').split('|')) * excel_data['3 or 4'][i] * (60/excel_data['Tempo'][i]) * sr)
        y = y[cutdown_start : cutdown_start + cutdown_len]
        soundfile.write(cutdown_music, y, sr)
        print(f"Cutting down finished!")
    else:
        print(f"File already cut!")

for i in range(len(excel_data)):
    if os.path.isfile(os.path.join(npy_path, f"{excel_data['Title'][i]}.npz")):
        print(f"{excel_data['Title'][i]}.npz exists, imported successfully!")
    else:
        print(f"{excel_data['Title'][i]}.npz not exists, preprocessing ... ", end='')
        
        padding_chord_list = ccchord.chord_padding(excel_data['Chords'][i])
        for c in range(len(padding_chord_list)):
            padding_chord_list[c] = ccchord.chord_simplify(padding_chord_list[c])
            padding_chord_list[c] = ccchord.chord_numeralize(padding_chord_list[c], capo=excel_data['Capo'][i])
        numerized_chords = np.array(padding_chord_list)

        y, sr = librosa.load(os.path.join(cutdown_path, f"{excel_data['Title'][i]}.wav"))
        music = ccpreprocess.Music(excel_data['Title'][i], y, sr, excel_data['Tempo'][i], sections=len(numerized_chords)//4,
                                    beats_per_section=4, slices_per_beat=excel_data['3 or 4'][i],
                                    f_min=-24, f_max=12, A4=440)
        amplitude_matrix = music.extract_amplitude_matrix()

        np.savez(os.path.join(npy_path, f"{excel_data['Title'][i]}"), x=amplitude_matrix, y=numerized_chords)
        print(f" npz complete!")
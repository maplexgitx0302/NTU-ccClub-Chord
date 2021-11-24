import os, time, sched
import numpy as np
import librosa
import sounddevice as sd
import ccchord

dir_path     = os.path.abspath('')
cutdown_path = os.path.join(dir_path, 'music_cutdown')

def play_sound(y, sr, stop_time=-1):
    s = sched.scheduler(time.time, time.sleep)
    if stop_time != -1:
        s.enter(stop_time, priority=0, action=sd.stop)
    sd.play(y / np.max(np.abs(y)), sr)
    s.run()


def display_chord(music_data, delay=0.4, stop_time=-1):
    original_chord_list = music_data['Chords'].strip('|').replace(' ', '').split('|')
    padding_chord_list = ccchord.chord_padding(chord_str=music_data['Chords'])
    
    y, sr = librosa.load(os.path.join(cutdown_path, f"{music_data['Title']}.wav"))
    second_per_tempo = 60 / music_data['Tempo']
    s = sched.scheduler(time.time, time.sleep)

    assert len(padding_chord_list)%4==0, "Please check the len of your chord string (chord list)"
    for i in range(len(padding_chord_list)//4):
        section_chord_str = ""
        for j in range(4):
            section_chord_str += padding_chord_list[4*i+j] + ' '*(12-len(padding_chord_list[4*i+j]))
        
        if stop_time != -1 and 4*i*second_per_tempo > stop_time:
            break
        
        s.enter(delay=4*i*second_per_tempo, priority=1, action=print, argument=(section_chord_str,))
        for t in range(4*music_data['3 or 4']):
            second_per_slice = second_per_tempo/music_data['3 or 4']
            print_dot = '|' + '.'*(12//music_data['3 or 4']-1)
            if t == 4*music_data['3 or 4'] - 1:
                s.enter(delay=4*i*second_per_tempo + second_per_slice*t, priority=1, action=print, argument=(print_dot,), kwargs={'end':'\n'})
            else:
                s.enter(delay=4*i*second_per_tempo + second_per_slice*t, priority=1, action=print, argument=(print_dot,), kwargs={'end':''})
    print(f"Now playing {music_data['Title']} with Key={music_data['Tune']} and Capo={music_data['Capo']}")
    play_sound(y, sr, stop_time)
    time.sleep(delay)
    s.run()
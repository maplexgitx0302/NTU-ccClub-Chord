'''
    ccplay is for playing music, audio files, chords:
    * please check you have device to play sound, otherwise 'sounddevice' cannot be used
    * note the delay time of 'display_chord' should be depends on different devices
'''

import os, time, sched
import numpy as np
import librosa
import sounddevice as sd
import ccchord

dir_path     = os.path.abspath('')
trim_path = os.path.join(dir_path, 'music_trim')

def play_sound(y, sr, stop_time=-1):
    '''
        y : np.array of wav file
        sr : sample rate
        stop_time : stop time of music playing, if -1 then play all

        - abstract -
        1. set up when to stop the music
        2. normalize the wav array with max(abs(array))=1
        3. play the music with 'sounddevice'
    '''
    s = sched.scheduler(time.time, time.sleep)
    if stop_time != -1:
        s.enter(stop_time, priority=0, action=sd.stop)
    sd.play(y / np.max(np.abs(y)), sr) # normalize the wav array
    s.run()


def display_chord(music_data, delay=0.4, stop_time=-1):
    '''
        music_data : a data of pandas read_excel format (same as the excel format)
        delay : since the music play will delay for a little time, we purposely delay the printed chords
        stop_time : stop time of printing chords

        - abstract -
        1. transform the chord string and pad it
        2. load the music with librosa and count the time per tempo
        3. set up when to print the chords
        4. set the delay time to let printing chords and playing music are simultaneously
    '''
    # transform the chord string into chord list, and also pad the chords
    original_chord_list = music_data['Chords'].strip('|').replace(' ', '').split('|')
    padding_chord_list  = ccchord.chord_padding(chord_str=music_data['Chords'])
    
    y, sr = librosa.load(os.path.join(trim_path, f"{music_data['Title']}.wav"))
    second_per_tempo = 60 / music_data['Tempo']
    s = sched.scheduler(time.time, time.sleep)

    assert len(padding_chord_list)%4==0, "Please check the len of your chord string (chord list)"
    for i in range(len(padding_chord_list)//4):
        section_chord_str = ""
        for j in range(4):
            # print each chord and pad it to len=12
            section_chord_str += padding_chord_list[4*i+j] + ' '*(12-len(padding_chord_list[4*i+j]))
        
        if stop_time != -1 and 4*i*second_per_tempo > stop_time:
            # print until the music stopped
            break
        
        # print chords and print the process line (|..|..|..|..)
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
    time.sleep(delay) # delay the printing chords to match with the music
    s.run()
import os
import numpy as np

class ChordError(Exception):
    def __init__(self, chord_str=''):
        self.chord_str = chord_str
        super().__init__()
    def __str__(self):
        return f"Please Check Your Chord -> {self.chord_str}"

pitch_index = [
    ['C', 'B#'],
    ['C#', 'Db'],
    ['D'],
    ['D#', 'Eb'],
    ['E', 'Fb'],
    ['F', 'E#'],
    ['F#', 'Gb'],
    ['G'],
    ['G#', 'Ab'],
    ['A'],
    ['A#', 'Bb'],
    ['B', 'Cb']
]

pitch_dict = {}
for i in range(len(pitch_index)):
    for pitch_name in pitch_index[i]:
        pitch_dict[pitch_name] = i

def chord_simplify(chord_str):
    if '/' in chord_str:
        chord_str = chord_str[:chord_str.index('/')]

    chord_set = set(list(chord_str))
    chord_major = {'C', 'D', 'E', 'F', 'G', 'A', 'B', '#', 'b'}
    chord_minor = chord_major.union({'m'})
    if chord_major.union(chord_set) == chord_major or chord_minor.union(chord_set) == chord_minor:
        # already major chord or minor chord
        return chord_str
    elif 'maj7' in chord_str or 'sus4' in chord_str:
        # strange chords to explicitly transform
        return chord_str
    elif '7' in chord_str:
        # x7, x7-5, x7+5 -> x7
        return chord_str[:chord_str.index('7')] + '7'
    elif 'm' in chord_str:
        return chord_str[:chord_str.index('m')] + 'm'
    elif '#' in chord_str:
        return chord_str[:chord_str.index('#')] + '#'
    elif 'b' in chord_str:
        return chord_str[:chord_str.index('b')] + 'b'
    else:
        # strange chords we do NOT want
        strange_chord = ['sus2', 'add9', '11']
        for chord in strange_chord:
            if chord in chord_str:
                return chord_str[0]
        else:
            raise ChordError(chord_str)

def chord_numeralize(capo, chord_str):
    main_key = chord_str[0]
    if '#' in chord_str:
        main_key += '#'
    elif 'b' in chord_str:
        main_key += 'b'

    chord_array = np.zeros(12)
    pitch = int((pitch_dict[main_key] + capo) % 12)
    if main_key == chord_str:
        # major : 1 3 5
        chord_array[pitch] += 1
        chord_array[(pitch + 4)%12] += 1
        chord_array[(pitch + 4 + 3)%12] += 1
    elif len(main_key) == len(chord_str) - 1 and chord_str[-1] == 'm':
        # minor : 1 b3 5
        chord_array[pitch] += 1
        chord_array[(pitch + 3)%12] += 1
        chord_array[(pitch + 3 + 4)%12] += 1
    elif 'sus4' in chord_str:
        # sus4 : 1 4 5
        chord_array[pitch] += 1
        chord_array[(pitch + 5)%12]
        chord_array[(pitch + 5 + 2)%12] += 1
    elif 'maj7' in chord_str:
        # maj7 : 1 3 5 7
        chord_array[pitch] += 1
        chord_array[(pitch + 4)%12] += 1
        chord_array[(pitch + 4 + 3)%12] += 1
        chord_array[(pitch + 4 + 3 + 4)%12] += 1
    elif 'm7' in chord_str:
        # m7 : 1 b3 5 b7
        chord_array[pitch] += 1
        chord_array[(pitch + 3)%12] += 1
        chord_array[(pitch + 3 + 4)%12] += 1
        chord_array[(pitch + 3 + 4 + 3)%12] += 1
    elif '7' in chord_str:
        # 7 : 1 3 5 b7
        chord_array[pitch] += 1
        chord_array[(pitch + 4)%12] += 1
        chord_array[(pitch + 4 + 3)%12] += 1
        chord_array[(pitch + 4 + 3 + 3)%12] += 1
    else:
        raise ChordError(chord_str)
    return chord_array / np.linalg.norm(chord_array)
'''
    ccchord is for transforming the chord strings and turn in to classic chords:
    * see whether you need to add or remove specific chords
'''

import numpy as np

# map the pitch to number (index), e.g. C->0 , D->2 , E->3 , .etc
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

# create a dictionary to return the number (index) of pitch
pitch_dict = {}
for i in range(len(pitch_index)):
    for pitch_name in pitch_index[i]:
        pitch_dict[pitch_name] = i

def chord_padding(chord_str):
    '''
        chord_str : chord string in the excel format

        - abstract -
        1. turn chord string into chord list
        2. pad the chords
    '''
    # transform the chord string into chord list
    original_chord_list = chord_str.strip('|').replace(' ', '').split('|')
    padding_chord_list = []
    for i in range(len(original_chord_list)):
        section_chord_list = original_chord_list[i].split(',')
        # length of chords per section should be 1 or 2 or 4
        if len(section_chord_list) == 1:
            # [C] -> [C,C,C,C]
            padding_chord_list += section_chord_list * 4
        elif len(section_chord_list) == 2:
            # [C,G] -> [C,C,G,G]
            padding_chord_list.append(section_chord_list[0])
            padding_chord_list.append(section_chord_list[0])
            padding_chord_list.append(section_chord_list[1])
            padding_chord_list.append(section_chord_list[1])
        elif len(section_chord_list) == 4:
            # [C,G,Am,F] -> [C,G,Am,F]
            padding_chord_list += section_chord_list
        else:
            assert False, f"Please check your chord string pairs (chord list) -> {section_chord_list}"
    return padding_chord_list

def chord_simplify(chord):
    '''
        chord : single chord string in the chord list
        
        - abstract -
        1. throw out the additional root if contains '/'
        2. keep maj7 and sus4
        3. turn every other thing that contains '7' into just '7'
        4. turn every other thing that contains 'm' into just 'm'
        5. turn every other thing that contains '#' into just '#'
        6. turn every other thing that contains 'b' into just 'b'
        7. turn every other strange chords into major root
    '''
    if '/' in chord:
        chord = chord[:chord.index('/')]

    chord_set = set(list(chord))
    chord_major = {'C', 'D', 'E', 'F', 'G', 'A', 'B', '#', 'b'}
    chord_minor = chord_major.union({'m'})
    if chord_major.union(chord_set) == chord_major or chord_minor.union(chord_set) == chord_minor:
        # already major chord or minor chord
        return chord
    # elif 'maj7' in chord or 'sus4' in chord:
    #     # strange chords to explicitly transform
    #     return chord
    # elif '7' in chord:
    #     # x7, x7-5, x7+5 -> x7
    #     return chord[:chord.index('7')] + '7'
    elif 'm' in chord and 'dim' not in chord and 'maj' not in chord:
        return chord[:chord.index('m')] + 'm'
    elif '#' in chord:
        return chord[:chord.index('#')] + '#'
    elif 'b' in chord:
        return chord[:chord.index('b')] + 'b'
    else:
        # strange chords we do NOT want
        strange_chord_list = ['sus2', 'add9', '11', 'maj7', 'sus4', '7', 'dim']
        for strange_chord in strange_chord_list:
            if strange_chord in chord:
                return chord[0]
        else:
            assert False, print(f"Please Check Your Chord -> {chord}")

def chord_numeralize(chord, capo=0, major_pitch_weight=1):
    '''
        chord : single chord string in the chord list
        capo  : capo of the song

        - abstract -
        1. find the major root
        2. convert in to a normalized array (sum=1)
    '''
    main_key = chord[0]
    if '#' in chord:
        main_key += '#'
    elif 'b' in chord:
        main_key += 'b'

    chord_array = np.zeros(12)
    pitch = int((pitch_dict[main_key] + capo) % 12)
    if main_key == chord:
        # major : 1 3 5
        chord_array[pitch] += 1 * major_pitch_weight
        chord_array[(pitch + 4)%12] += 1
        chord_array[(pitch + 4 + 3)%12] += 1
    elif len(main_key) == len(chord) - 1 and chord[-1] == 'm':
        # minor : 1 b3 5
        chord_array[pitch] += 1 * major_pitch_weight
        chord_array[(pitch + 3)%12] += 1
        chord_array[(pitch + 3 + 4)%12] += 1
    # elif 'sus4' in chord:
    #     # sus4 : 1 4 5
    #     chord_array[pitch] += 1 * major_pitch_weight
    #     chord_array[(pitch + 5)%12]
    #     chord_array[(pitch + 5 + 2)%12] += 1
    # elif 'maj7' in chord:
    #     # maj7 : 1 3 5 7
    #     chord_array[pitch] += 1 * major_pitch_weight
    #     chord_array[(pitch + 4)%12] += 1
    #     chord_array[(pitch + 4 + 3)%12] += 1
    #     chord_array[(pitch + 4 + 3 + 4)%12] += 1
    # elif 'm7' in chord:
    #     # m7 : 1 b3 5 b7
    #     chord_array[pitch] += 1 * major_pitch_weight
    #     chord_array[(pitch + 3)%12] += 1
    #     chord_array[(pitch + 3 + 4)%12] += 1
    #     chord_array[(pitch + 3 + 4 + 3)%12] += 1
    # elif '7' in chord:
    #     # 7 : 1 3 5 b7
    #     chord_array[pitch] += 1 * major_pitch_weight
    #     chord_array[(pitch + 4)%12] += 1
    #     chord_array[(pitch + 4 + 3)%12] += 1
    #     chord_array[(pitch + 4 + 3 + 3)%12] += 1
    else:
        assert False, print(f"Please Check Your Chord -> {chord}")
    # return chord_array / np.linalg.norm(chord_array)
    return chord_array / np.sum(chord_array)

def chord_inverse(chord_nparray, num_candidate=3, capo=0):
    '''
    
    '''
    candidate_pitch = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    candidate_chord = []
    capo_pitch = []
    for i in range(12):
        capo_pitch.append(candidate_pitch[(i-capo)%12])
    # suffix = ['', 'm', 'sus4', 'maj7', 'm7', '7']
    suffix = ['', 'm']
    for i in range(len(candidate_pitch)):
        for j in range(len(suffix)):
            chord = chord_numeralize(candidate_pitch[i]+suffix[j], capo=0, major_pitch_weight=1)
            candidate_chord.append([capo_pitch[i]+suffix[j], chord])
    
    def cos_loss(y_pred, y_true):
        cos = (np.dot(y_pred, y_true))/(np.linalg.norm(y_pred)*np.linalg.norm(y_true))
        return -cos

    candidate_chord.sort(key=lambda x: cos_loss(chord_nparray, x[1]))
    if num_candidate == 1:
        return candidate_chord[0][0]
    else:
        return [x[0] for x in candidate_chord[:num_candidate]]
'''
    ccpreprocess is to preprocess the data:
    * zip all the information of the song into a class 'Music'
'''

import os, time
import numpy as np
import librosa

dir_path = os.path.dirname(__file__)
trim_path = os.path.join(dir_path, 'music_trim')

def softmax(matrix):
    '''
        matrix : default to be designed for amplitude matrix
        
        - abstract -
        1. extract with the maximum with each frame
        2. count the softmax for each frame
    '''
    x = matrix - np.max(matrix, axis=1).reshape(-1,1)
    exp_x = np.exp(x)
    sum_x = np.sum(exp_x, axis=1).reshape(-1,1)
    return exp_x / sum_x

class Music():
    def __init__(self, title, tempo, sections, beats_per_section, slices_per_beat,
                f_min=-36, f_max=27, A4=440):
        '''
            title : title of the song
            tempo : beats per minute (bpm)
            sections : number of sections to simplify
            beats_per_section : number of beats per section
            slices_per_beat : number of slices per beat
            f_min : minimum frequency to analyze (default=A1)
            f_max : maximum frequency to analyze (default=C7)
            A4 : default Hz of A4

            - abstract -
            1. set up every information of the song
            2. use fft to count the amplitude in frequency space
            3. if needed, use com 'composite_wave' to listen to the fft audio
        '''
        y, sr = librosa.load(os.path.join(trim_path, f"{title}.wav"))
        self.y = y
        self.sr = sr
        self.title = title
        self.tempo = tempo
        self.sections = sections
        self.beats_per_section = beats_per_section
        self.slices_per_beat = slices_per_beat
        self.length_per_slice = int(60 / tempo * sr / slices_per_beat) # the length of the array per slice
        self.ks = [A4 * 2**(f/12) for f in range(f_min, f_max+1)] # target frequencies to be analyzed

    def extract_amplitude_matrix(self, normalized=True):
        '''
            normalized : whether devide the amplitude matrix with the maximum value

            - abstract -
            1. select the target frame to be analyzed with fft
            2. use numpy fft and get the right frequency

            - mathematical detail -
            A(f) = Sum_t(A(t)*exp(-2*i*pi*f*t))   # theoretical
            A(k) = Sum_m(A(m)*exp(-2*i*pi*m*k/n)) # numpy fft
            By t = m * (1/sr), e.g. t=1 -> m=sr, we get f/sr = k/n
            Finally k = n*f/sr, where k is the index in numpy fft result

            ref : https://numpy.org/doc/stable/reference/routines.fft.html#module-numpy.fft
        '''
        amplitude_matrix = []
        total_frames = self.slices_per_beat * self.beats_per_section * self.sections

        for frame in range(total_frames):
            # target frame
            start_index = frame * self.length_per_slice
            end_index   = (frame+1) * self.length_per_slice

            # start fft
            fft = np.abs(np.fft.fft(self.y[start_index:end_index]))
            amplitude = np.array([fft[round((end_index-start_index)*k/self.sr)] for k in self.ks])
            amplitude_matrix.append(amplitude)
        amplitude_matrix = np.array(amplitude_matrix)
        
        if normalized:
            amplitude_matrix = amplitude_matrix / np.max(np.abs(amplitude_matrix))
        
        return np.array(amplitude_matrix)

    def composite_wave(self, amplitude_matrix):
        '''
            amplitude_matrix : the fft analyzed amplitudes of the target frequencies

            - abstract -
            1. pad (repeat) the amplitude matrix and then transpose 
            2. superposed with sine waves
        '''

        total_frames   = self.slices_per_beat * self.beats_per_section * self.sections
        total_length   = self.length_per_slice * total_frames
        wave_amplitude = np.repeat(amplitude_matrix, self.length_per_slice, axis=0).T
        superposition  = np.zeros(total_length)
        for i in range(len(self.ks)):
            k = self.ks[i]
            superposition += wave_amplitude[i] * np.sin(2 * np.pi * k * np.arange(total_length) / self.sr)
        return superposition
# Predicting Chords with Machine Learning

## About the project
In this project (see 'project' directory above), we use modern machine learning skills to build a model, and try to predict the chords of a given song. The input data (data fed into the model) will be the **Fourier Frequency Amplitude** extracted from the training data (see the *.xlsx* file) using Fourier analysis. The output (prediction) of the model will be chords, which will be transformed into a numeric array.

See slide introduction of the project : [ccClub - Chord](https://docs.google.com/presentation/d/1WBkZJQ0kPvZTtnDEnendAcTQ_kkzUiDXsWbk2ehmlug/edit?usp=sharing)

---

## Prerequisites
This project is mainly written in **Python**, recommended version between 3.6.x~3.9.x

1. Please check whether you have [*ffmpeg*](http://www.ffmpeg.org/download.html)

2. It is highly recommended to use **Juperter Lab** (or Jupyter Notebook) to run this project. To install, 
    ```
    python -m pip install jupyterlab openpyxl
    ```

3. The packages we need is written in `requirements.txt`, to install,
    ```
    python -m pip install -r requirements.txt
    ```

---

## Get started
1. Open file `ccmain.ipynb`

2. The first time you run `ccmain.ipynb` will download music data (*.wav*) from the internet, it may take a few minutes.

3. Change the hyperparameters of the model, or try different structure.

4. Predict the chords of a song with the trained model.

---

## Python Scripts Description

* `ccdownload.py` : Downloading video from the internet and transform into *.wav* format using *ffmpeg*.

* `ccplay.py` : Read the wave array and play the music with packages **Librosa**, **Sounddevice**.

* `ccchord.py` : Anything related to chords, e.g. transforming chords into numeric numpy arrays, filtering chords we need.

* `ccpreprocess.py` : Preprocessing the data we need, such as using **Fourier Analysis** to extract the wave amplitude with some target frequencies.


'''
    ccdownload is for downloading files we need:
    * Please make sure you have 'ffmpeg' in local.
    * YouTube has change something, if pytube is not work correctly, see:
        https://stackoverflow.com/questions/70060263/pytube-attributeerror-nonetype-object-has-no-attribute-span
'''

import os
import subprocess # for using 'ffmpeg' in terminal
from pytube import YouTube # for downloading YouTube mp4 files

dir_path   = os.path.abspath('') # directory path of the ccClub project
if os.path.isdir(os.path.join(dir_path, 'music_original')) == False:
    os.mkdir(os.path.join(dir_path, 'music_original'))
music_path = os.path.join(dir_path, 'music_original') # directory path for saving wav files

def yt_wav(link, title=''):
    '''
        link  : YouTube link (url)
        title : name of the wav files

        - abstract -
        1. use pytube to get youtube object
        2. download the lowest resolution video
        3. convert the video into audio with 'ffmpeg'
    '''
    yt = YouTube(link)
    if title == '': title = yt.title
    input_mp4  = os.path.join(music_path, f'{title}.mp4')
    output_wav = os.path.join(music_path, f'{title}.wav')
    print(f'Now processing {title} ... ', end='')
    if not os.path.isfile(output_wav):
        print('Downloading ... ', end='')
        ys = yt.streams.get_lowest_resolution()
        ys.download(output_path=music_path, filename=f'{title}.mp4')
        print('Converting to wav ... ', end='')
        # use local 'ffmpeg' to transform mp4 into wav
        subprocess.run(['ffmpeg', '-hide_banner', '-loglevel', 'error', '-y' ,'-i', input_mp4, output_wav])
        subprocess.run(['rm', input_mp4])
        print(f'Complete!')
    else:
        print(f'File already exists!')

example_music = os.path.join(music_path, 'example_music.wav')
if __name__ == '__main__':
    # example_link = 'https://www.youtube.com/watch?v=PLHXWAkvi7Q' # Crispy 脆樂團 (Cover 教學) 魏如萱&馬頔 - 星期三或禮拜三 
    example_link = 'https://www.youtube.com/watch?v=LPVHVR4kO_M' # 告五人 Accusefive - 爱在夏天 demo
    if os.path.isfile(example_music):
        subprocess.run(['rm', example_music])
    yt_wav(example_link, 'example_music')
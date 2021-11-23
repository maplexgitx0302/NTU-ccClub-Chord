import os
import re
import subprocess
from pytube import YouTube

dir_path   = os.path.abspath('') # directory path of the ccClub project
if os.path.isdir(os.path.join(dir_path, 'music_original')) == False:
    os.mkdir(os.path.join(dir_path, 'music_original'))
music_path = os.path.join(dir_path, 'music_original') # directory path for saving wav files

def yt_wav(link, file_name=''):
    yt = YouTube(link)
    if file_name == '': file_name  = yt.title
    file_name = re.sub('[/,\,.,-,?,!,@,#,$,%,^,&,*,~,`,(,),\[,\]]', '', file_name)
    input_mp4  = os.path.join(music_path, f'{file_name}.mp4')
    output_wav = os.path.join(music_path, f'{file_name}.wav')
    print(f'Now processing {file_name} ... ', end='')
    if not os.path.isfile(output_wav):
        print('Downloading ... ', end='')
        ys = yt.streams.get_lowest_resolution()
        ys.download(output_path=music_path, filename=f'{file_name}.mp4')
        print('Converting to wav ... ', end='')
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
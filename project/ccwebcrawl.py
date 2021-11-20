import os
import requests
from selenium import webdriver

dir_path = os.path.dirname(os.path.realpath(__file__)) # directory path of the ccClub project

def yt_playlist(playlist_url):
    print(f'Now crawling {playlist_url} ... ', end='')
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    driver = webdriver.Chrome(os.path.join(dir_path, 'chromedriver'), options=options)
    driver.get(playlist_url)
    urls = []

    elems = driver.find_elements_by_xpath("//a[@href]")
    for elem in elems:
        url = elem.get_attribute("href")
        if 'index' in url and url not in urls:
            urls.append(url)
    driver.quit()
    print(f'Done!')
    return urls

example_url = 'https://www.youtube.com/playlist?list=FLxe1OE4q9YkjuyYT0rjgaUA'
if __name__ == '__main__':
    urls = yt_playlist(example_url)
    for url in urls:
        print(url)
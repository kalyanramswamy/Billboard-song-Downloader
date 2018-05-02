from __future__ import unicode_literals
from bs4 import BeautifulSoup
from html.parser import HTMLParser
from tqdm import tqdm
import youtube_dl
import requests
import sqlite3
import os
import sys

# directory to download songs
downloadDir = "/Users/kalyan_cont2/songs/new"

url = 'http://www.billboard.com/charts/hot-100'
response = requests.get(url)
html = response.content

songs_list = []
conn = sqlite3.connect('bilboards.db')

# Create Table song_list

try:
    conn.execute('''CREATE TABLE song_list
           (ID INTEGER PRIMARY KEY   AUTOINCREMENT,
           song_title    TEXT    UNIQUE,
           download_status  INT     default 0,
           download_url TEXT);''')
except Exception as e:
    pass

billboard = BeautifulSoup(html, 'html.parser')
for article in billboard.findAll('article', {"class": "js-chart-row"}):
    try:
        full_song_name = []
        song_name = article.find('h2').text
        if (len(song_name.strip()) !=0): full_song_name.append(song_name.strip()) 
        artist = article.find('a').text
        if (len(artist.strip()) !=0): full_song_name.append(artist.strip())
        full_song_name.append('lyrics')
        if "Featuring" in artist:
            artist = artist.split("Featuring")[0]
        html_parser = HTMLParser()
        song = html_parser.unescape((' '.join(map(str,full_song_name))).strip())
        songs_list.append(song)
        try:
            conn.execute("INSERT INTO song_list(song_title) VALUES (?);", (song,))
            conn.commit()
        except Exception as e:
            pass
    except Exception as e:
        pass

# get song url from youtube
def search_youtube(name):
    song_name = name.replace(" ", "+")

    url = "https://www.youtube.com/results?search_query="+song_name
    response = requests.get(url)
    html = response.content

    soup = BeautifulSoup(html, 'html.parser')
    for atag in soup.findAll('h3',attrs={'class':'yt-lockup-title '}):
        video_code = atag.find('a')['href']
        if video_code.find('&list') >=0 :
            video_code = video_code[:video_code.find('&')]
        song_url = 'https://www.youtube.com'+ video_code
        break
    return song_url


# store youtube video url in database
songs = conn.execute("SELECT id, song_title from song_list where download_url is null")
for row in songs:
    try:
        download_url = search_youtube(row[1])
        if (download_url.find("&") < 0) & (download_url.find("channel") < 0):
            conn.execute("UPDATE song_list set download_url=(?) where id=(?);", (download_url,row[0],))
            conn.commit()
    except Exception as e:
        pass

def blockPrint():
    sys.stdout = open(os.devnull, 'w')

def enablePrint():
    sys.stdout = sys.__stdout__

# download from youtube

download_list = conn.execute("SELECT id, download_url, song_title from song_list where download_status is 0").fetchall()
print("downloading...")
for row in tqdm(download_list):
    download_url = row[1]
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    os.chdir(downloadDir)
    blockPrint()
    try:
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([download_url])
        conn.execute("UPDATE song_list set download_status=(?) where id=(?);", (1,row[0],))
        conn.commit()
    except Exception as e:
        pass
    enablePrint()

conn.close()
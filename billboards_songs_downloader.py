from __future__ import unicode_literals
from BeautifulSoup import BeautifulSoup
from HTMLParser import HTMLParser
import youtube_dl
import requests
import sqlite3
import os

# directory to download songs
downloadDir = "/home/kalyan/bilboards"

url = 'http://www.billboard.com/charts/hot-100'
response = requests.get(url)
html = response.content

songs_list = []
conn = sqlite3.connect('BILBOARDS.db')

# Create Table bilboard_list
# try:
#     conn.execute('''CREATE TABLE bilboard_list
#            (ID INTEGER PRIMARY KEY   AUTOINCREMENT,
#            Song_title    TEXT    UNIQUE,
#            download_status  INT     default 0,
#            download_url TEXT);''')
#     print "Table created successfully";
# except Exception as e:
#     raise e

billboard = BeautifulSoup(html)
for article in billboard.findAll('article'):
    try:
        song_name = str(article['data-songtitle'])
        artist = article.find('a').text
        if "Featuring" in artist:
            artist = artist.split("Featuring")[0]
        html_parser = HTMLParser()
        song = html_parser.unescape((song_name+' '+artist))        
        songs_list.append(song)
        try:
            conn.execute("INSERT INTO bilboard_list (Song_title) VALUES (?);", (song,))
            conn.commit()
        except Exception as e:
            print("song already in list")      
    except Exception as e:
        print "---not a song article---"

# get song url from youtube
def search_youtube(name):
    song_name = name.replace(" ", "+")

    url = "https://www.youtube.com/results?search_query="+song_name
    response = requests.get(url)
    html = response.content

    soup = BeautifulSoup(html)
    for atag in soup.findAll('h3',attrs={'class':'yt-lockup-title '}):
        song_url = 'https://www.youtube.com'+atag.find('a')['href']
        break
    return song_url


# store youtube video url in database
songs = conn.execute("SELECT id, song_title from bilboard_list where download_url is null")
for row in songs:
    try:
        download_url = search_youtube(row[1])
        print(download_url)
        conn.execute("UPDATE bilboard_list set download_url=(?) where id=(?);", (download_url,row[0],))
        conn.commit()
    except Exception as e:
        print("Error occurred")


# download from youtube

download_list = conn.execute("SELECT id, download_url,Song_title from bilboard_list where download_status is 0")
for row in download_list:
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
    try:
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([download_url])
        print("Finish downloading "+row[2])
        conn.execute("UPDATE bilboard_list set download_status=(?) where id=(?);", (1,row[0],))
        conn.commit()
    except Exception as e:
        print("fail to download")


conn.close()
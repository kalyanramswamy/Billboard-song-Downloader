# Billboard songs downloader: Download Hot 100 billboard songs
For lazy song lovers

## Getting Started

Billboard songs downloader helps you download HOT 100 songs.
you can improve this code by scheduling to run every week which can download newly added songs to the list.

### Requirements
* Python
* packages required
  * Sqlite 3
  * BeautifulSoup 4
  * youtube_dl

```
use pip to install these packages

pip install sqlite3
pip install beautifulsoup
pip install youtube_dl

to convert audio to mp3
sudo apt-get install -y libav-tools (Linux)
brew install libav (osX)

```

Then Run
```
python billboards_songs_downloader.py

```


## How it works
* scrape [Billboard Hot 100 songs](http://www.billboard.com/charts/hot-100) titles.
* then download songs from youtube using youtube_dl

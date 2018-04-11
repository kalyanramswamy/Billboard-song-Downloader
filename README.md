# Billboard songs downloader: Download Hot 100 billboard songs
For lazy song lovers

## Getting Started

Billboard songs downloader helps you download HOT 100 songs.
you can improve this code by scheduling it to run every week, this will help you download new songs.

### Requirements
* Python 2.7
* packages required
  * Sqlite 3
  * BeautifulSoup 3.2
  * youtube_dl
  * requests
  * HTMLParser
  * os

```
use pip to install these packages

pip install sqlite3
pip install beautifulsoup
pip install youtube_dl

```

Then Run
```
python billboards_songs_downloader.py

```


## How it works
* scrape [Billboard Hot 100 songs](http://www.billboard.com/charts/hot-100) titles.
* then download songs from youtube using youtube_dl

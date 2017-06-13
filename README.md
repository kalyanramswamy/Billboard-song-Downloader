# Billboard songs downloader: Download Hot 100 billboard songs
For lazy song lovers

## Getting Started

Billboard songs downloader helps you download HOT 100 songs.
you can improve the code by scheduling it to run every week, this will help you download new songs.

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


```
run
python billboards_songs_downloader.py

```


## How it works
* Source: [Billboard Hot 100 songs](http://www.billboard.com/charts/hot-100)
* Store song titles in database for future references
* Get song url for youtube
* Using youtube_dl download mp3
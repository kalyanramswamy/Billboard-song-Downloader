# Billboard songs downloader: Download Hot 100 billboard songs
For lazy song lovers

## Getting Started

Billboard songs downloader helps you download HOT 100 songs.
you can improve the code by scheduling it to run every week, this will help you download new songs.

### Requirements
* Python 2.7
* Sqlite 3
* packages required
  * BeautifulSoup
  * requests
  * HTMLParser
  * os

```
use pip to install these packages
```

## How it works
* Get Billboard Hot 100 songs from [here](http://www.billboard.com/charts/hot-100)
* store song titles in database for future references
* get song official url for youtube
* using youtube_dl download mp3
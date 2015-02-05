# Webcrawler built using scrapy


Installation
=======

`sudo pip install scrapy`


Running the crawler
=======

Choose which spider you want to run. 

Scrap the entire web page, follow all links and all tracks:
lyricsspider/spiders/wiki.py

Scrap only the top artist pages and their lyrics:
lyricsspider/spiders/top_artist.py

Give a set of artists:
lyricsspider/spiders/selected_artist.py



run with
scrapy crawl <spider_name>


output will be written to lyricsspider/output




Take care when crawling, respect that you are putting load on the webpage.
DISCLAIMER:
I take no personal resposibility of how this code is used or executed.
I'm only proving how it could be done.

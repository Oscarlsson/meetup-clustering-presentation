import scrapy
import re

from scrapy.contrib.spiders import CrawlSpider
from lyricsspider.items import Lyric


# Scraps everything from song lyrics
class SelectedArtistsSpider(CrawlSpider):

    """ Maybe not every lyric is important
    """
    artist = ['bob-dylan',
              'katy-perry',
              'justin-bieber',
              'kiss',
              'aerosmith',
              'lady-gaga',
              'led-zeppelin',
              'madonna',
              'maroon-5',
              'red-hot-chili-peppers',
              'taylor-swift',
              'the-ramones',
              'U2',
              'one-direction',
              'the-kooks',
              'jake-bugg',
              'arctic-monkeys',
              'the-streets',
              'westlife',
              'backstreet-boys',
              'hanson-brothers']

    name = 'selected_artists'
    base_url = 'www.songlyrics.com'
    allowed_domains = [base_url]
    start_urls = ['http://' + base_url + '/taylor-swift-lyrics']

    def parse(self, response):
        for artist_ in self.artist:
            url = 'http://' + self.base_url + '/%s-lyrics' % artist_
            yield scrapy.http.Request(url, callback=self.parse_artistpage)

    def parse_artistpage(self, response):
        lyriclinks = response.xpath('//table[@class=\'tracklist\']')[0].css('a[href*=-lyrics\/]::attr(href)').extract()
        for url in lyriclinks[:40]:
            if not url.startswith('http://'):
                continue
            yield scrapy.http.Request(url, callback=self.parse_lyrics)

    # parse lyrics
    def parse_lyrics(self, response):
        title = response.xpath("//h1/text()").extract()[0].split(" - ")
        lyric = response.xpath("//p[@id='songLyricsDiv']/text()").extract()
        if len(title) == 2:
            artist, track = title
        elif len(title) > 2:
            artist = title[0]
            track = " ".join(title[:0])

        return Lyric(artist=artist, track=track, lyric=lyric)

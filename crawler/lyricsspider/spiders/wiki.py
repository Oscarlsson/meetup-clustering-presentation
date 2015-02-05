import scrapy
import string

from scrapy.contrib.spiders import CrawlSpider
from lyricsspider.items import Lyric


# Scraps everything from song lyrics
class WikiSpider(CrawlSpider):

    """ Scraps everything
    """

    name = 'wiki'
    allowed_domains = ['www.songlyrics.com']
    base_url = 'http://www.songlyrics.com/'
    start_urls = ['http://www.songlyrics.com/a']

    # for each /a to /z
    def parse(self, response):
        for c in string.ascii_lowercase:
            print self.base_url + c
            # return scrapy.http.Request(self.base_url + c, callback=self.parse_multiartistpage)
            yield scrapy.http.Request(self.base_url + c, callback=self.parse_multiartistpage)

    #  for each artist on page
    def parse_multiartistpage(self, response):
        artistlinks = response.xpath('//table[@class=\'tracklist\']')[0].css('a[href*=-lyrics\/]::attr(href)').extract()
        for url in artistlinks:
            if not url.startswith('http://'):
                continue
            # return scrapy.http.Request(url, callback=self.parse_artistpage)
            yield scrapy.http.Request(url, callback=self.parse_artistpage)

    # for each lyric
    def parse_artistpage(self, response):
        lyriclinks = response.xpath('//table[@class=\'tracklist\']')[0].css('a[href*=-lyrics\/]::attr(href)').extract()
        for url in lyriclinks:
            if not url.startswith('http://'):
                continue
            # return scrapy.http.Request(url, callback=self.parse_lyrics)
            yield scrapy.http.Request(url, callback=self.parse_lyrics)

    # parse lyrics
    def parse_lyrics(self, response):
        # This can crash! Too many values if - in the name
        title = response.xpath("//h1/text()").extract()[0].split(" - ")
        if len(title) == 2:
            artist, track = title
        elif len(title) > 2:
            track = title[-1]
            artist = " ".join(title[:-1])

            lyric = response.xpath("//p[@id='songLyricsDiv']/text()").extract()
            return Lyric(artist=artist, track=track, lyric=lyric)

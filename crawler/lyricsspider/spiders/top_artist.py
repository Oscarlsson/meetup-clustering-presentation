import scrapy
import re

from scrapy.contrib.spiders import CrawlSpider
from lyricsspider.items import Lyric


# Scraps everything from top artists
class TopArtistSpider(CrawlSpider):

    """ Maybe not every lyric is important
    """
    artist = []
    name = 'top_artist'
    base_url = 'www.songlyrics.com'
    allowed_domains = [base_url]
    start_urls = ['http://' + base_url + '/news/top-songs/2011']

    def parse(self, response):
        links = set(response.xpath('//div[@class="listbox"]').css('a::attr(href)').extract())
        for link in links:
            yield scrapy.http.Request(link, callback=self.parse_toppage)

    def parse_toppage(self, response):
        artist_and_lyrics = response.xpath('//table[@class=\'tracklist\']')[0].css('a[href*=-lyrics\/]::attr(href)').extract()
        for artist_or_lyric in artist_and_lyrics:
            if re.search(self.base_url + '/[a-zA-Z0-9-]*-lyrics/$', artist_or_lyric):
                pass
                yield scrapy.http.Request(artist_or_lyric, callback=self.parse_artistpage)
            else:
                yield scrapy.http.Request(artist_or_lyric, callback=self.parse_lyrics)

    def parse_artistpage(self, response):
        lyriclinks = response.xpath('//table[@class=\'tracklist\']')[0].css('a[href*=-lyrics\/]::attr(href)').extract()
        for url in lyriclinks:
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

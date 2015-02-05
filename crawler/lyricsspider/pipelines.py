# -*- coding: utf-8 -*-

import json
import os

from scrapy.exceptions import DropItem


class outputter(object):
    basepath = 'output'

    def __init__(self):
        self.ids_seen = set()
        if not os.path.exists(self.basepath):
            os.makedirs(self.basepath)

    def artist_exist(self, artist):
        directory = self.basepath + '/%s' % artist
        return os.path.exists(directory)

    def track_exist(self, artist, track):
        directory = self.basepath + '/%s' % artist
        filepath = directory + '/%s.json' % track
        return os.path.isfile(filepath)

    def process_item(self, item, spider):
        artist = item['artist']
        track = item['track']
        lyric = item['lyric']  # list

        if artist:
            if track:
                if lyric:
                    directory = self.basepath + '/%s' % artist
                    # New artist, create dir
                    if not self.artist_exist(artist):
                        os.makedirs(directory)

                    # Track includes ' Lyrics'
                    track = track.rstrip(' Lyrics')
                    filepath = directory + '/%s.json' % track

                    # Dont save same lyric twice if re-run
                    if not self.track_exist(artist, track):
                        file_ = open(filepath, 'wb')
                        line = json.dumps(dict(item)) + "\n"
                        file_.write(line)
                        return item
                else:
                    raise DropItem("Missing lyric in %s" % item)
            else:
                raise DropItem("Missing track in %s" % item)
        else:
            raise DropItem("Missing artist in %s" % item)

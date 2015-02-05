import pandas as pd
import simplejson as json
import re
import os
import sys

def build_dataset(debug=False):
    allowed_artists = ['Bob Dylan', 
                        'Katy Perry',
                        'Justin Bieber',
                        'Kiss',
                        'Aerosmith',
                        'Lady Gaga',
                        'Led Zeppelin',
                        'Madonna',
                        'Maroon 5',
                        'Red Hot Chili Peppers',
                        'Taylor Swift',
                        'The Ramones',
                        'U2',
                        'One Direction']
    columns=['artist', 'track', 'lyric']
    dt = pd.DataFrame(columns=columns)
    artists = os.listdir('../crawler/output')
    filtered_artists = filter(lambda artist: artist in allowed_artists, artists)
    for artist in filtered_artists:
        if artist in allowed_artists:
            if debug:
                print "======== ARTIST ======="
                print artist
                print "======== LYRICS ======="
                
            lyrics = os.listdir('../crawler/output/%s' % artist)
            for lyric_name in lyrics[:10]:
                lyric_file = '../crawler/output/%s/%s' % (artist, lyric_name)
                with open(lyric_file) as f:
                    lyric = json.load(f)
                if debug:
                    print "saving ..", 
                    print lyric
                
                dt.loc[len(dt)+1] = [lyric['artist'], lyric['track'], " ".join(lyric['lyric'])]
            
    return dt

def data_cleaning(dataset):
    dataset['lyric'] = dataset['lyric'].apply(lambda lyric: re.sub('\\n', '', lyric))
    dataset['lyric'] = dataset['lyric'].apply(lambda lyric: re.sub('\\r', '', lyric))
    dataset['lyric'] = dataset['lyric'].apply(lambda lyric: re.sub('.?\[.*?\] | \(.*?\)', '', lyric))
    dataset['lyric'] = dataset['lyric'].apply(lambda lyric: lyric.lower())
    dataset['track'] = dataset['track'].apply(lambda track: track.lower().rstrip('lyrics'))
    dataset['artist'] = dataset['artist'].apply(lambda artist: artist.lower())
    return dataset

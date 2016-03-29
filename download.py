import argparse
import os
import logging
import sys

from urllib.request import urlopen
from concurrent.futures import ThreadPoolExecutor
from pymongo import MongoClient

# http://luoo-mp3.kssws.ks-cdn.com/low/luoo/radio805/01.mp3
# http://luoo-mp3.kssws.ks-cdn.com/low/luoo/radio5/01.mp3
BASE_URL = 'http://luoo-mp3.kssws.ks-cdn.com/low/luoo/radio'

client = MongoClient()
db = client.luoo

logger = logging.getLogger('download')
logger.setLevel(logging.DEBUG)

fh = logging.FileHandler('luoo.log')
fh.setLevel(logging.DEBUG)

ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s')

fh.setFormatter(formatter)
ch.setFormatter(formatter)

logger.addHandler(fh)
logger.addHandler(ch)


def download(song, basedir='luoo_download'):
    logger.info(('downloading ', song['vol_number'], song['trackname']))
    try:
        dirpath = os.path.join(
            basedir, song['vol_number'] + '_' + song['vol_title'])
        if not os.path.exists(dirpath):
            os.makedirs(dirpath)
        url = BASE_URL + str(int(song['vol_number'])) + '/' + \
            song['trackname'].split('.')[0] + '.mp3'
        data = urlopen(url).read()
        filename = os.path.join(
            dirpath, song['trackname'] + '_' + song['artist'] + '.mp3')
        if os.path.exists(filename):
            raise FileExistsError(filename)
        with open(filename, 'wb') as f:
            f.write(data)
        logger.info(('download complete', song[
                    'vol_number'], song['trackname']))
    except Exception as inst:
        logger.error(
            ('download error', song['vol_number'], song['trackname'], inst))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--min", type=int, default=0,
                        help="min number to download")
    parser.add_argument("--max", type=int,
                        help="max number to download")
    args = parser.parse_args()

    songs = []
    if args.max is None:
        songs = [song for song in db.music.find(
            {'vol_number': {'$gt': str(args.min)}})]
    elif args.max > 0:
        songs = [song for song in db.music.find(
            {'vol_number': {'$gt': str(args.min), '$lt': str(args.max)}})]

    with ThreadPoolExecutor(max_workers=4) as executor:
        executor.map(download, songs)


if __name__ == '__main__':
    main()

#!/usr/bin/env python3

import requests
import ujson as json
import time
import logging
import sqlite3

logging.basicConfig(level=logging.DEBUG)
logging.getLogger("urllib3").setLevel(logging.WARNING)

class tiktok:

    def __init__(self):
        self.default_retries = 25


    def make_request(self, url, **kwargs):
        '''Generic method to fetch data from tiktok's private API'''

        # Set Headers
        headers = {}
        headers['referer'] = "https://www.tiktok.com"
        headers['user-agent'] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.70 Safari/537.36"
        headers['Content-Type'] = "application/json"

        # Set Parameters
        params = {}
        params['_signature'] = "URNT6AAgEB1mf0XznNI7b1ETUvAAAyq"
        params.update(kwargs)

        retries = self.default_retries

        while retries:
            r = requests.get(url, headers=headers, params=params)
            data = r.json()
            if data['statusCode'] != 0:
                retries -= 1
                logging.debug("Empty content received. Retrying. ({} attempts left)".format(retries))
                time.sleep(.25)
                continue
            else:
                return r.json()


    def comment_list(self, id, count=48, cursor=0):
        '''Method to fetch comments for a specific video id.

            Required Parameters:

                id: (video id)
                count: (number of comments to return)
                cursor: (cursor position)

            URL Endpoint: https://www.tiktok.com/share/item/comment/list

        '''
        url = "https://www.tiktok.com/share/item/comment/list"
        params = {}
        params['id'] = id
        params['count'] = count
        params['cursor'] = cursor

        data = self.make_request(url, **params)
        return data['body']


    def fetch_all_comments(self, video_id):
        '''Method to fetch all available comments for a video id.

        Required Parameters to API endpoint:

            id: (video id)
        '''

        hasMore = True
        cursor = 0

        while hasMore:
            data = self.comment_list(id=video_id, cursor=cursor)
            for comment in data['commentListData']:
                yield comment

            hasMore = data['hasMore']
            cursor = data['cursor']


    def item_list(self, type=5, count=42, minCursor=0, maxCursor=0):
        '''Method to fetch items from TikTok

            Required Parameters:

                id: (Not sure what this is but needs to be passed -- set to null or 0)

            Unknown Parameters:

                type:       ???
                shareUid:   ???
                secUid:     ???

            URL Endpoint: https://www.tiktok.com/share/item/list
            '''

        url = "https://www.tiktok.com/share/item/list"

        params = {}
        params['id'] = 0
        params['count'] = count
        params['type'] = type
        params['minCursor'] = minCursor
        params['maxCursor'] = maxCursor

        data = self.make_request(url, **params)
        return data['body']


    def fetch_all_items(self):
        '''Method to fetch all available items (trending)'''

        hasMore = True
        minCursor = 0
        maxCursor = 0

        while hasMore:
            data = self.item_list(minCursor=minCursor, maxCursor=maxCursor)
            for item in data['itemListData']:
                yield item

            hasMore = data['hasMore']
            minCursor = data['minCursor']
            maxCursor = data['maxCursor']



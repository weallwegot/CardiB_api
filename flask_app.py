from flask import Flask, request, url_for, render_template
from flask import jsonify, session, current_app
from flask_restful import reqparse, abort, Api, Resource
from flask_cors import CORS, cross_origin
import json
import requests
import urllib2
import lxml.html
import random
import urllib.request, urllib.error, urllib.parse

app = Flask(__name__)
app.secret_key = "v9rex04(_2n(e4ae?xd3xec=x1dda3bd+=1x92xe290-xf6x93Lxf3_kjdh78fu4bc"
#api
api = Api(app)
#cors for cross origin headers 
CORS(app)

"""
LyricalApi class takes a get request
parses the keys, if the artist key is present
look up random lyric from said artist
if its not, look up random lyric from Cardi B
"""
class LyricalApi(Resource):
    def get(self):
        json_data = request.get_json()
        if 'artist' not in json_data.keys():
            artist = 'cardi-b'
        else:
            artist = json_data['artist']
        lyric, song = get_random_lyric(artist)
        return {'meta':{'code':200},'data':{'lyric':lyric, 'song':song}}

def get_random_lyric(artist_string):
    if len(artist_string) > 0:
        first_letter = artist_string[0]
        base_url_for_az_lyrics = 'http://www.azlyrics.com/'
        artist_specific_url = base_url_for_az_lyrics + first_letter + '/' + artist_string + '.html'
        page = requests.get(artist_specific_url)
        page_tree = lxml.html.fromstring(all_articles_page.content)
        all_a_tags = page_tree.xpath('//html//a')




api.add_resource(BotAPI, '/api/v1')


if __name__ == "__main__":
    app.run()
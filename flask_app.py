from flask import Flask, request, url_for, render_template
from flask import jsonify, session, current_app
from flask_restful import reqparse, abort, Api, Resource
from flask_cors import CORS, cross_origin
import json
import requests
import lxml.html
import random
import os

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
        # this is not a post, so there is not json data..
        json_data = {'artist':'none'}#request.get_json()
        if 'artist' not in json_data.keys():
            artist = 'cardi-b'
        else:
            artist = json_data['artist']
        lyric, song = get_random_lyric(artist)
        return {'meta':{'code':200},'data':{'lyric':lyric, 'song':song}}

def get_random_lyric(artist_string):
    if len(artist_string) > 0:
        # first_letter = artist_string[0]
        # base_url_for_az_lyrics = 'http://www.azlyrics.com/'
        # artist_specific_url = base_url_for_az_lyrics + first_letter + '/' + artist_string + '.html'
        # page = requests.get(artist_specific_url)
        # page_tree = lxml.html.fromstring(all_articles_page.content)
        # all_a_tags = page_tree.xpath('//html//a')
        working_dir = os.path.dirname(os.path.abspath(__file__))
        data_folder_path = working_dir + os.sep + "data_bc_webscraper_blocked" + os.sep + "cardi_b"
        g = os.listdir(data_folder_path)
        song_file_name = random.choice(g)
        txt_file = open(data_folder_path+os.sep+song_file_name,'r').readlines()
        # for line in txt_file:
        #     print(line + "Length: " + str(len(line)))
        while(True):
            ind = random.choice(range(len(txt_file)))
            half_bar_1 = txt_file[ind]
            half_bar_2 = txt_file[ind+1]
            if (len(half_bar_1) == 1 ) or (len(half_bar_2) == 1):
                continue
            else:
                break
        bar = half_bar_1+ ', '+half_bar_2
        song = song_file_name[:-4].replace('_'," ")
        return bar, song


@app.route('/')
def hello_world():
    return 'Hello You Have Reached The Cardi B Lyrics Api, send a get request to "cardibbars.pythonanywhere.com/api/v1"!'
# print(str(get_random_lyric('b')))



api.add_resource(LyricalApi, '/api/v1')


if __name__ == "__main__":
    app.run()
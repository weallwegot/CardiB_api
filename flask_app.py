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
app.secret_key = "a_long_secret"
#api
api = Api(app)
#cors for cross origin headers 
CORS(app)

# the directory of the curent file
working_dir = os.path.dirname(os.path.abspath(__file__))
# the data folder
data_folder_path = working_dir + os.sep + "data_bc_webscraper_blocked"
# valid folder options as post values
valid_options = ['james_baldwin','cardi_b','jay_z','nas','coding_quotes','kanye_west','lauryn_hill','tupac']

"""
LyricalApi class takes a get request
parses the keys, if the artist key is present
look up random lyric from said artist
if its not, look up random lyric from Cardi B
"""
class LyricalApi(Resource):
    def get(self):
        lyric, song, artist = get_random_lyric()
        return {'meta':{'code':200},'data':{'lyric':lyric, 'song':song, 'author':artist}}
    def post(self):
        json_data = request.get_json()
        if 'method' in json_data.keys() and 'category' in json_data.keys():
            method_string = json_data['method'] # right now this is unused
            category_list = json_data['category'] # this is the "category" of quote. could be an artist or genre or inspirational
            print(str(category_list))
            if len(category_list) == 0:
                category_list = None
            lyric, song, artist = get_random_lyric(category_list)
            if lyric == song  == artist:
                error_msg = 'You passed an invalid argument. Use one of the following ' + str(valid_options)
                return {'meta':{'code':400},'error':{'code':400,'message':error_msg}}
            else:
                return {'meta':{'code':200},'data':{'lyric':lyric, 'song':song, 'author':artist}}
        else:
            
            error_msg = 'Please include a category key in your JSON with an array specifying the type of random quote you would like.'
            error_msg += ' Your options are as follows: ' + str(valid_options)
            error_msg += ' Or, use a GET request with no parameters.'
            return {'meta':{'code':400},'error':{'code':400,'message':error_msg}}

def get_random_lyric(category_array=None):
    # if there are no arguments, we will pick something random from db/.txt files
    if not category_array:
        # first_letter = artist_string[0]
        # base_url_for_az_lyrics = 'http://www.azlyrics.com/'
        # artist_specific_url = base_url_for_az_lyrics + first_letter + '/' + artist_string + '.html'
        # page = requests.get(artist_specific_url)
        # page_tree = lxml.html.fromstring(all_articles_page.content)
        # all_a_tags = page_tree.xpath('//html//a')

        txt_file,song,cat_folder= drill_down_and_get_file_and_song()

        quote_or_lyric, author = piece_necessary_info_together(txt_file,song)

        if not author:
            # if the author isnt determined in method above then it is the category folder name
            # split on _, get rid of 'lyric' or 'quote' [:-1], then make one string joined by space from list
            author = ' '.join(cat_folder.split('_')[:-1])

        return quote_or_lyric, song, author
    else:
        valid_options = ['james_baldwin','cardi_b','jay_z','nas','inspirational_code','kanye_west','lauryn_hill','tupac']
        valid_options_passed_in = set(valid_options) & set(category_array)
        if len(valid_options_passed_in) == 0:
            error_msg = 'You passed an invalid argument. Use one of the following ' + str(valid_options)
            return '','',''
            #
        else:
            chosen_option = random.choice(list(valid_options_passed_in))
            all_options_folder_names = os.listdir(data_folder_path)
            chosen_option_quote = chosen_option+'_quotes'
            chosen_option_lyrics = chosen_option+'_lyrics'
            if chosen_option_lyrics in all_options_folder_names:
                the_file,the_song,cat_folder = drill_down_and_get_file_and_song(chosen_option_lyrics)
                quote_or_lyric, author = piece_necessary_info_together(the_file,the_song)

            elif chosen_option_quote in all_options_folder_names:
                the_file,the_song,cat_folder = drill_down_and_get_file_and_song(chosen_option_quote)
                quote_or_lyric, author = piece_necessary_info_together(the_file,the_song)

            if not author:
                # if the author isnt determined in method above then it is the category folder name
                # split on _, get rid of 'lyric' or 'quote' [:-1], then make one string joined by space from list
                author = ' '.join(cat_folder.split('_')[:-1])

            return quote_or_lyric, the_song, author
        
def drill_down_and_get_file_and_song(category_file_name_arg=None):
    # the directory of the curent file
    working_dir = os.path.dirname(os.path.abspath(__file__))
    # the data folder
    data_folder_path = working_dir + os.sep + "data_bc_webscraper_blocked"
    # a random category within the folder
    if not category_file_name_arg:
        sub_directories_of_data = [sub_dir for sub_dir in os.listdir(data_folder_path) if '.' not in sub_dir]
        catetgory_file_name = random.choice(sub_directories_of_data)
    else:
        catetgory_file_name = category_file_name_arg

    # the path to the category
    path_to_chosen_category = data_folder_path + os.sep + catetgory_file_name
    # a random file within the chosen category
    last_file_name = random.choice(os.listdir(path_to_chosen_category))
    # full path to txt file
    full_path = path_to_chosen_category+os.sep+last_file_name
    my_file = open(full_path,'r').readlines()

    potential_song = ''
    # if the file isnt a lyrics 
    if 'quotes' in catetgory_file_name.split('_'):
        potential_song = ''
    elif 'lyrics' in catetgory_file_name.split('_'):
        #cut out the .txt
        potential_song = last_file_name[:-4].replace('_'," ")

    return my_file,potential_song,catetgory_file_name

def are_bars_valid(bars_list):
    check_if_bar_is_bad = lambda a:'[' in a or ']' in a or len(a) == 1 or '(' in a or ')' in a
    truth_array = [not check_if_bar_is_bad(bar) for bar in bars_list]
    return all(truth_array)

def is_valid_quote_author_combo(combo_list_quote_first_author_second):
    # the files have quote in front of the quotes
    # and authors in front of the authors
    # so check for them.
    l = combo_list_quote_first_author_second
    return 'QUOTE' in l[0].split(':')[0].upper() and 'AUTHOR' in l[1].split(':')[0].upper()

def piece_necessary_info_together(txt_file_lines,song):
    # if it is a song expect the bar format, where 2 lines make a bar
    if len(song) > 0:
        while(True):
            ind = random.choice(range(len(txt_file_lines)-4))
            half_bar_1 = txt_file_lines[ind]
            half_bar_2 = txt_file_lines[ind+1]
            half_bar_3 = txt_file_lines[ind+2]
            half_bar_4 = txt_file_lines[ind+3]
            bars_all = [half_bar_1,half_bar_2,half_bar_3,half_bar_4]
            if not are_bars_valid(bars_all):
                continue
            else:
                break
        bar = half_bar_1+half_bar_2+half_bar_3+half_bar_4
        author = None
        # author is left blank bc its a song, the author is in the parent directory name
        return bar, author
    # its not a song so expect a quote and an author
    else:
        while(True):
            ind = random.choice(range(len(txt_file_lines)-1))
            hopefully_quote = txt_file_lines[ind]
            hopefully_author = txt_file_lines[ind+1]
            hopeful_combo = [hopefully_quote,hopefully_author]
            if not is_valid_quote_author_combo(hopeful_combo):
                continue
            else:
                break
        quote = hopefully_quote[6:]
        author = hopefully_author[7:]
        return quote, author

        


@app.route('/')
def hello_world():
    return 'Hello You Have Reached The Cardi B Lyrics Api, send a get request to "cardibbars.pythonanywhere.com/api/v1"!'
# print(str(get_random_lyric('b')))



api.add_resource(LyricalApi, '/api/v1')


if __name__ == "__main__":
    app.run()

import boto3
import s3fs
import json
import logging
import re
import random

from constants import VALID_OPTIONS, SAFE_4_WORK
from utilities import contains_curse

print('Loading function')

import boto3 
s3 = boto3.client("s3")
my_s3fs = s3fs.S3FileSystem()
toplevel_dir = "s3://bars-api/just-lyrics/"


def respond(err, res=None):
    return {
        'statusCode': '400' if err else '200',
        'body': err.message if err else json.dumps(res),
        'headers': {
            'Content-Type': 'application/json',
            "Access-Control-Allow-Origin" : "*" #Required for CORS support to work
        },
    }


def lambda_handler(event, context):
    '''Demonstrates a simple HTTP endpoint using API Gateway. You have full
    access to the request and response payload, including headers and
    status code.

    '''

    operations = {
        'GET': 'get_method()',
        'POST': 'post_method()'
    }

    operation = event['httpMethod']
    if operation in operations:
        if operation == 'GET':
        
            lyric, song, artist = get_random_lyric()
            logging.debug('lyric: {}\nsong: {}\nartist: {}\n'.format(lyric,song,artist))
            payload = {'meta':{'code':200},'data':{'lyric':lyric, 'song':song, 'author':artist}}
            
            return respond(err=None,res=payload)
            
            
        elif operation == 'POST':
            json_data = request.get_json()
            if 'method' in json_data.keys() and 'category' in json_data.keys():
                method_string = json_data['method'] # right now this is unused
                category_list = json_data['category'] # this is the "category" of quote. could be an artist or genre or inspirational
                logging.debug('arguments passed: {}'.format(category_list))
                if len(category_list) == 0:
                    category_list = None
                lyric, song, artist = get_random_lyric(category_list)
                if lyric == song  == artist:
                    error_msg = 'You passed an invalid argument. Use one of the following {}'.format(VALID_OPTIONS)
                    logging.error(error_msg)
                    payload = {'meta':{'code':400},'error':{'code':400,'message':error_msg}}
                else:
                    payload = {'meta':{'code':200},'data':{'lyric':lyric, 'song':song, 'author':artist}}
            else:
    
                error_msg = 'Please include a category key in your JSON with an array specifying the type of random quote you would like.'
                error_msg += ' Your options are as follows: \n{}'.format(VALID_OPTIONS)
                error_msg += ' Or, use a GET request with no parameters.'
                logging.error(error_msg)
                payload = {'meta':{'code':400},'error':{'code':400,'message':error_msg}}
                
            return response(err=None,res=payload)
        
        
        return respond(err=None, res=operations[operation])
    
    
    else:
        return respond(ValueError('Unsupported method "{}"'.format(operation)))
        
        
        
def get_random_lyric(category_array=[]):
    """
    if there are no arguments, we will pick something random from db/.txt files
    or if there is one argument and it is the safe for work option
    """
    logging.debug('Category Array: '+str(category_array))
    # pdb.set_trace()
    # user wants curses if safe for work not in the category array
    wants_curses = not SAFE_4_WORK in category_array
    # if safe for work is only element in array, then get any song from any artist without curse words
    if (category_array == []) or ((len(category_array)==1) and (SAFE_4_WORK in category_array)):

        txt_file,song,cat_folder = drill_down_and_get_file_and_song()

        quote_or_lyric, author = piece_necessary_info_together(txt_file,song,wants_curses)

        if not author:
            # if the author isnt determined in method above then it is the category folder name
            # split on _, get rid of 'lyric' or 'quote' [:-1], then make one string joined by space from list
            author = ' '.join(cat_folder.split('_')[:-1])
            # this depends on old naming convention of 'artistname _lyrics'
            # if this returns nothing or blank string, use cat folder
            if author in ['',' ']:
                author = cat_folder

        logging.debug('Returning author: '+author)
        logging.debug('Cat folder was: '+cat_folder)
        logging.debug('Returning quote or lyric'+quote_or_lyric)
        logging.debug('Returning song'+song)

        return quote_or_lyric, song, author
    else:
        # get the intersection of the available options and the options posted
        valid_options_passed_in = set(VALID_OPTIONS) & set(category_array)
        # wants_curses = True
        # # if user passes in SAFE_4_WORK parameter then they dont want any cursing in the bars
        # if SAFE_4_WORK in valid_options_passed_in:
        #     wants_curses = False
        if len(valid_options_passed_in) == 0:
            error_msg = 'You passed an invalid argument. Use one of the following: {}'.format(VALID_OPTIONS)
            logging.error("Passed Invalid Args Message: {}".format(error_msg))
            return '','',''
        else:
            if not wants_curses:
                # remove safe for work so it doesnt get picked in the random author selection
                valid_options_passed_in.remove(SAFE_4_WORK)
            chosen_option = random.choice(list(valid_options_passed_in))
            all_options_folder_names = os.listdir(data_folder_path)
            chosen_option_quote = chosen_option+'_quotes'
            chosen_option_lyrics = chosen_option+'_lyrics'
            logging.debug('Chosen option: '+chosen_option)
            logging.debug('valid options passed in: '+str(valid_options_passed_in))
            if chosen_option_lyrics in all_options_folder_names:
                the_file,the_song,cat_folder = drill_down_and_get_file_and_song(chosen_option_lyrics)

            elif chosen_option in all_options_folder_names:
                the_file,the_song,cat_folder = drill_down_and_get_file_and_song(chosen_option)

            elif chosen_option_quote in all_options_folder_names:
                the_file,the_song,cat_folder = drill_down_and_get_file_and_song(chosen_option_quote)
                
            quote_or_lyric, author = piece_necessary_info_together(the_file,the_song,wants_curses)

            if not author:
                # if the author isnt determined in method above then it is the category folder name
                # split on _, get rid of 'lyric' or 'quote' [:-1], then make one string joined by space from list
                author = ' '.join(cat_folder.split('_')[:-1])
                logging.debug('***** HIT SPLIT AUTHOR LOGIC*****')
                # this depends on old naming convention of 'artistname _lyrics'
                # if this returns nothing or blank string, use cat folder
                if author in [' ','']:
                    logging.debug('***** HIT BLANK AUTHOR LOGIC*****')
                    author = cat_folder
            logging.debug('Returning author: '+author)
            logging.debug('Cat folder was: '+cat_folder)
            logging.debug('Returning quote or lyric'+quote_or_lyric)
            logging.debug('Returning song'+the_song)

            return quote_or_lyric, the_song, author

def drill_down_and_get_file_and_song(category_file_name_arg=None,wants_curses=True):
    # the directory of the curent file
    #working_dir = os.path.dirname(os.path.abspath(__file__))
    # the data folder
    #data_folder_path = working_dir + os.sep + "data_bc_webscraper_blocked"
    #bucket = s3.bucket('bars-api')
    #logging.debug("Reached data folder path: {}".format(data_folder_path))
    # a random category within the folder
    if not category_file_name_arg:
        # ignore folders that have dots in them, not sure what this would be.
        
        sub_directories_of_data = my_s3fs.ls(toplevel_dir)

        # sub_directories_of_data = [sub_dir for sub_dir in os.listdir(data_folder_path) if '.' not in sub_dir]
        category_file_name = random.choice(sub_directories_of_data)
    else:
        category_file_name = category_file_name_arg

    # the path to the folder that contains data to said category
    path_to_chosen_category = category_file_name
    #path_to_chosen_category = data_folder_path + os.sep + catetgory_file_name
    # a random file within the chosen category
    last_file_name = random.choice(my_s3fs.ls(category_file_name))
    #last_file_name = random.choice(os.listdir(path_to_chosen_category))
    if not wants_curses:
        song_has_curse_word = contains_curse(last_file_name)
        while not song_has_curse_word:
            # last_file_name = random.choice(os.listdir(path_to_chosen_category))
            last_file_name = random.choice(my_s3fs.ls(category_file_name))
            song_has_curse_word = contains_curse(last_file_name)
    # full path to txt file
    #full_path = path_to_chosen_category+os.sep+last_file_name
    full_path = last_file_name
    logging.debug("Reached full path: {}".format(full_path))
    
    with my_s3fs.open(full_path,'r') as fl:
        my_file_lines = fl.readlines()
    
    #my_file = open(full_path,'r')
    #my_file_lines = my_file.readlines()
    #my_file.close()

    potential_song = ''
    # if the file isnt a lyrics the text file will be saved with a quotes in line ending
    if 'quotes' in category_file_name.split('_'):
        potential_song = ''
    elif 'lyrics' in category_file_name.split('_') or '_' not in category_file_name:
        #cut out the .txt
        potential_song = last_file_name[:-4].replace('_'," ")

    return my_file_lines,potential_song,category_file_name

def are_bars_valid(bars_list,cursing_allowed=True):
    """
    Check to make sure the lines chosen don't have
    something like the artists name in brackets
    or [2x] or anything like that. We want a meaningful 4 lines
    Also check for the album info for the new type of folders
    """
    check_if_bar_is_bad = lambda a:'[' in a or ']' in a or len(a) == 1 or '(' in a or ')' in a
    bar_validity_truth_array = [not check_if_bar_is_bad(bar) for bar in bars_list]
    if not cursing_allowed:

        curse = contains_curse(''.join(bars_list))
        logging.debug('Contained a curse? {}'.format(curse))
        return (not curse) & all(bar_validity_truth_array)

    return all(bar_validity_truth_array)

def is_valid_quote_author_combo(combo_list_quote_first_author_second):
    """
    the files have quote in front of the quotes
    and authors in front of the authors
    so check for them.
    """
    l = combo_list_quote_first_author_second
    return 'QUOTE' in l[0].split(':')[0].upper() and 'AUTHOR' in l[1].split(':')[0].upper()

def piece_necessary_info_together(txt_file_lines,song,wants_curses=True):
    # if it is a song expect the bar format, where 2 lines make a bar
    if len(song) > 0:
        while(True):
            # find out where the album info piece is and exclude it from random choice
            try:
                idx_of_album_info = txt_file_lines.index('ALBUM INFO\r\n')
            except ValueError:
                #not every text file will have album info i.e. mixtapes and stuff
                idx_of_album_info = len(txt_file_lines)

            num_useful_lines = idx_of_album_info
            logging.debug("Index of Last Useful Line: {}".format(num_useful_lines))
            logging.debug("Number of lines in song: {}".format(len(txt_file_lines)))
            # up to the 4 before the end of useful lines so we can construct a whole bar
            ind = random.choice(range(num_useful_lines-4))
            half_bar_1 = txt_file_lines[ind]
            half_bar_2 = txt_file_lines[ind+1]
            half_bar_3 = txt_file_lines[ind+2]
            half_bar_4 = txt_file_lines[ind+3]
            bars_all = [half_bar_1,half_bar_2,half_bar_3,half_bar_4]
            logging.info(bars_all)
            if not are_bars_valid(bars_all,cursing_allowed=wants_curses):
                continue
            else:
                break
        bar = half_bar_1+half_bar_2+half_bar_3+half_bar_4
        logging.info("Valid bar composed: {}".format(bar))
        author = None
        # author is left blank bc its a song, the author is in the parent directory name
        return bar, author
    # its not a song so expect a quote and an author
    else:
        """
        This is strange but okay.
        Choose a random index from the file and hope that it is a quote
        and then hope that the next line is an author lol
        If it's not try another random index and hope some more.
        Repeat until hope == reality

        I don't understand why the mod%2 operator wasnt used
        since this file has all authors on even line numbers.
        Maybe thats not always a valid assumption, I don't know.
        Will all the quotes always be on one line?
        This very clearly needs to be ported to a DB
        """
        while(True):
            ind = random.choice(range(len(txt_file_lines)-1))
            hopefully_quote = txt_file_lines[ind]
            hopefully_author = txt_file_lines[ind+1]
            hopeful_combo = [hopefully_quote,hopefully_author]
            if not is_valid_quote_author_combo(hopeful_combo):
                continue
            else:
                break
        # cut out the number of letters in the word "quote " (peep the space)
        quote = hopefully_quote[6:]
        # cut out the number of letters in the word "author " (peep the space)
        author = hopefully_author[7:]
        logging.info("Valid quote and author found: {} - {}".format(quote,author))
        return quote, author




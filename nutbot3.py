import os
import time
import requests
import json
import sqlite3
import datetime

from slackclient import SlackClient
from settings import SLACK_ID, SLACK_TOKEN, NUT_ID, NUT_KEY
from db import db_add_food, db_all_foods, db_daily_summary
from pprint import pprint
# import pandas as pd

# getting following vars from settings.py
# starterbot's ID as an environment variable
# BOT_ID = os.environ.get("NUTBOT_ID")
# NUT_ID = os.environ.get("NUT_API_ID")
# NUT_KEY = os.environ.get("NUT_API_KEY")
# BOT_TOKEN = os.environ.get("NUTBOT_TOKEN")


# constants
AT_BOT = "<@" + SLACK_ID + ">"
NUT_URL = 'https://trackapi.nutritionix.com/v2/natural/nutrients'
NUT_HEADERS = {
        "x-app-id": NUT_ID,
        "x-app-key": NUT_KEY,
        "x-remote-user-id": '0'
        }
EXAMPLE_COMMAND = ['add', 'summary']
FOOD_KEYS = {'nf_calories':'calories', 'food_name':'name', 'serving_qty':'quantity'}


# instantiate Slack clnt
slack_client = SlackClient(SLACK_TOKEN)

def get_users():
    """ returns dict of all users. key as uid and name as value """
    users_list = slack_client.api_call("users.list")
    if 'members' in users_list:
        users = { user['id'] : user['name'] for user in users_list['members'] } 
        return users


def filter_keys(dct, keys):
    new_dct = { new_key: dct[old_key] for old_key, new_key in keys.items() }
    new_dct['date_time'] = datetime.datetime.now()
    return new_dct



def handle_command(command, channel, user):
    """
        Receives commands directed at the bot and determines if they
        are valid commands. If so, then acts on the commands. If not,
        returns back what it needs for clarification.
    """
    response = "Not sure what you mean. Use the *" + "ADD" + \
               "* command with numbers, delimited by spaces."

    # slack_client.api_call("chat.postMessage", channel=channel, text=response, as_user=True)
    if command.startswith('summary'):
        handle_summary(channel) #post summary.

    else:
        handle_add(command, channel, user)



def handle_add(phrase, channel, user):
    """
       sends the phrase to Nut API and adds result to DB
    """
    response = send_nut_query(form_nut_query(phrase))
    
    #debugging
    #print (json.dumps(response, indent=4))
    
    if not response["foods"]:
        print("list of foods in api response is empty")
    
    message = ''

    # send slack msg wrt each food and add to DB
    for food in response["foods"]:
        # add msg
        add_msg = str(food["food_name"]) + " - " + str(food["serving_qty"]) + " - " + \
                  str(food["nf_calories"]) + '\n'
        message += add_msg
        
        # add to db
        db_add_food(filter_keys(food, FOOD_KEYS), user)

    slack_client.api_call("chat.postMessage", channel=channel, \
                text=message, as_user=True)
        
    
    # needs fix
    # if unmatched items exist, prompt to rephrase
    if 'unmatched' in response.keys() and response['unmatched']:
        message = "NutBot did not recognize " + response['unmatched'] + \
                "please rephrase the query"
        slack_client.api_call("chat.postMessage", channel=channel, text=response, as_user=True)
        

def handle_summary(channel):
    """
       returns summary of food consumed and report total calories
    """
    summary = ""
    calories = 0

    # needs to change sqlite to dict
    records = []
    for food in records:
        message = str(food["food_name"]) + " - " + str(food["serving_qty"]) + " - " + \
                  str(food["nf_calories"]) + "\n"
        summary = summary + message
        calories += food["nf_calories"]
    slack_client.api_call("chat.postMessage", channel=channel, text=summary, as_user=True)
    
    db_daily_summary()
    # db_all_foods() 
    
    # send total calories count
    calories_msg = "You had " + str(calories) + " calories"
    slack_client.api_call("chat.postMessage", channel=channel, text=calories_msg, as_user=True)


def parse_slack_output(slack_rtm_output):
    """
        The Slack Real Time Messaging API is an events firehose.
        this parsing function returns None unless a message is
        directed at the Bot, based on its ID.
    """
    output_list = slack_rtm_output
    # pprint(output_list) #testing
    if output_list and len(output_list) > 0:
        for output in output_list:
            # if msg text contains @nutbot
            if output and 'text' in output and AT_BOT in output['text']: 
                # return text after the @ mention, whitespace removed
                return output['text'].split(AT_BOT)[1].strip().lower(), \
                       output['channel'], output['user']

    return None, None, None




def send_nut_query(query):
    """
       Sends json query to Nutritionix API and returns result
    """
    response = requests.post(NUT_URL, data=query, headers=NUT_HEADERS)
    response_dict = response.json()
    # print ("NUT API response is: \n\n\n" + response.text)
    # print ("DICT ver: \n\n\n" + response_dict)

    return response_dict


def form_nut_query(phrase):
    """
       Parses phrase and forms appropriate dict query
       the Nutritionix NLP API parses command
    """
    query = {
        'query': phrase,
        #'appId': NUT_API_ID,
        #'appKey': NUT_API_KEY,
        #'fields': '*'
    }
    return query


if __name__ == "__main__":
    READ_WEBSOCKET_DELAY = 1 # 1 second delay between reading from firehose
    if slack_client.rtm_connect():
        print("StarterBot connected and running!")
        while True:
            command, channel, user = parse_slack_output(slack_client.rtm_read())
            if command and channel and user:
                handle_command(command, channel, user)
            time.sleep(READ_WEBSOCKET_DELAY)
    else:
        print("Connection failed. Invalid Slack token or bot ID?")

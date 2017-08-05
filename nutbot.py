import os
import time
from slackclient import SlackClient

import requests

# starterbot's ID as an environment variable
BOT_ID = os.environ.get("NUTBOT_ID")
NUT_ID = os.environ.get("NUT_API_ID")
NUT_KEY = os.environ.get("NUT_API_KEY")


# constants
AT_BOT = "<@" + BOT_ID + ">"

EXAMPLE_COMMAND = ['add', 'summary']

# instantiate Slack & Twilio clients
slack_client = SlackClient(os.environ.get('NUTBOT_TOKEN'))


def handle_command(command, channel):
    """
        Receives commands directed at the bot and determines if they
        are valid commands. If so, then acts on the commands. If not,
        returns back what it needs for clarification.
    """
    response = "Not sure what you mean. Use the *" + EXAMPLE_COMMAND + \
               "* command with numbers, delimited by spaces."
               
    if command.startswith('add'):
        phrase = command.split('add')[1]
        handle_add(phrase)

    # slack_client.api_call("chat.postMessage", channel=channel, text=response, as_user=True)
    if command.startswith('summary'):
        handle_summary() #post summary.

def handle_add(phrase):
    """
       sends the phrase to Nut API and adds result to dataframe.
    """
    result = send_nut_query(form_nut_query(phrase))
    # if not found item exits in result, prompt to rephrase
    # add to dataframe


def handle_summary():
    # query dataframe for relevant parameters
    # calculate total calories

def parse_slack_output(slack_rtm_output):
    """
        The Slack Real Time Messaging API is an events firehose.
        this parsing function returns None unless a message is
        directed at the Bot, based on its ID.
    """
    output_list = slack_rtm_output
    if output_list and len(output_list) > 0:
        for output in output_list:
            if output and 'text' in output and AT_BOT in output['text']:
                # return text after the @ mention, whitespace removed
                return output['text'].split(AT_BOT)[1].strip().lower(), \
                       output['channel']
    return None, None


if __name__ == "__main__":
    READ_WEBSOCKET_DELAY = 1 # 1 second delay between reading from firehose
    if slack_client.rtm_connect():
        print("StarterBot connected and running!")
        while True:
            command, channel = parse_slack_output(slack_client.rtm_read())
            if command and channel:
                handle_command(command, channel)
            time.sleep(READ_WEBSOCKET_DELAY)
    else:
        print("Connection failed. Invalid Slack token or bot ID?")


def send_nut_query(query):
    """
       Sends json query to Nutritionix API and returns result
    """
    url = 'https://api.nutritionix.com/v1_1/search'
    # need headers?
    r = requests.post(url, data=query)
    # r = requests.post(url, data=json.dumps(payload))
    print r.text
    return r


def form_nut_query(phrase):
    """
       Parses phrase and forms appropriate dict query
       the Nutritionix NLP API parses command
    """
    query = {
        'appId': NUT_API_ID,
        'appKey': NUT_API_KEY,
        'query': phrase,
        'fields': '*'
    }
    
    return query


        
        


    
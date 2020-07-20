import os
from emoji import UNICODE_EMOJI
# from datetime import datetime
import json
import random
import sys
from flask import Flask
app = Flask(__name__)
# $ set FLASK_APP=server.py
# $ flask run

JSON_ARRAY = []  # is populated at server start
JSON_FILENAME = "your-imessage-file.json"
HTML = "your-website.html"

ME = "IsFromMe"
FROM = "FromPhoneNumber"
TO = "ToPhoneNumber"
TIMESTAMP = "TextDate"
TEXT = "MessageText"

YOUR_NUM = "your-cell-number"
OTHER_NUM = "other-cell-number"

BADWORDS = ['list', 'negative', 'words', 'here'] # append words to add texts
NICEWORDS = ['list', 'nice', 'words', 'here'] # append words to add texts

COLORS = ['w3-ios-dark-blue', 'w3-ios-deep-blue', 'w3-ios-blue', 'w3-ios-light-blue', 'w3-ios-pink', 'w3-ios-orange']

def process_json_file():
    global JSON_ARRAY
    filename = JSON_FILENAME
    with open(filename, 'r', encoding='utf-8') as f:
        JSON_ARRAY = json.load(f)  # read a conversation as a list
    NICEWORDS.extend(UNICODE_EMOJI)  # include emojis


def isMean(text): # include pleasant chats, exclude arguments
    for niceword in NICEWORDS:
        if niceword not in text.lower():
            return True
        else:
            for badword in BADWORDS:
                if badword in text.lower():
                    return True
                else:
                    return False


def message():
    process_json_file()
    returnstring = ""
    randomtext = random.choice(JSON_ARRAY)
    while isMean(randomtext[TEXT]):  # loop until isMean(text) is False
        randomtext = random.choice(JSON_ARRAY)

    returnstring += "<p>" + randomtext[TIMESTAMP] + "</p>"
    returnstring += "<p>" + randomtext[TEXT] + "</p>"
    if randomtext[FROM] == YOUR_NUM:
        returnstring += '<p> - You </p>'
    elif randomtext[FROM] == OTHER_NUM:
        returnstring += '<p>- Other </p>'
    return returnstring


@app.route('/')
def html():
    with open(HTML, 'r', encoding='utf-8') as f:
        text = f.read()
        final = text.replace('inserttexthere', message())
        final = final.replace('insertcolorhere', str(random.choice(COLORS)))
        print(final)
        return final


def main():
    process_json_file()
    app.run(host="localhost", port=9999, debug=True)

if __name__ == "__main__":
    main()
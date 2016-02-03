import random
import requests
import json

from django.utils.html import escape


def japlugin(keyword, message):
    keyword_arr = keyword.split(' ')
    # if len(keyword_arr) != 2:
    #     return message

    trigger = keyword_arr[0]
    text = ' '.join(keyword_arr[1:])

    if 'translate' in trigger:
        response = requests.get('http://api.giphy.com/v1/gifs/translate?s=' + unicode(text) + '&api_key=dc6zaTOxFJmzC')
        response = json.loads(response.content)
        try:
            data = response['data']['images']['original']['url']
            return {
                'fallback': 'You seem to be bored.',
                'title': 'You seem to be bored.',
                'text': 'Say ' + text,
                'image_url': data
            }
        except:
            return {
                'fallback': 'You seem to be bored.',
                'title': 'You seem to be bored.',
                'text': 'Say' + message,
                'image_url': 'http://media3.giphy.com/media/cKwLWoHvmxcn6/giphy.gif'
            }
    return message

import random
import requests
import json


def japlugin(keyword, message):
    keyword_arr = keyword.split(' ')
    if len(keyword_arr) != 2:
        return message

    trigger = keyword_arr[0]
    server_name = keyword_arr[1]
    if trigger == 'refresh':
        response = requests.post('http://jaroku.thinkdwm.com/refresh/'+ server_name + '?token=7O_6qe65k9L2:LL37Y88Iy0K48H%2x')
        # response = json.loads(response.content)
        return {
            'fallback': 'Refresh Server ' + server_name,
            'title': server_name,
            'text': 'Updated!',
            'image_url': 'http://m.memegen.com/3qlg11.jpg'
        }

    return message

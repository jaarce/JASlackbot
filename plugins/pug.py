import random
import requests
import json


def japlugin(keyword, message):
    if keyword == 'pug me' or 'pug' in keyword:
        page = random.randint(0, 200)
        response = requests.get('https://api.flickr.com/services/rest/?method=flickr.photos.search&api_key=4952b7932b05d0c12f6ee23b6b47669a&text=dog%20pugs&format=json&page=' + str(page) + '&nojsoncallback=1')
        response = json.loads(response.content)
        # random from 1 to 100
        index = random.randint(0, 50)
        try:
            owner = response['photos']['photo'][index]['owner']
            image_id = response['photos']['photo'][index]['id']
            farm = response['photos']['photo'][index]['farm']
            secret = response['photos']['photo'][index]['secret']
            server = response['photos']['photo'][index]['server']
            return {
                'fallback': 'Cute pugs everywhere',
                'title': 'Pugs everywhere!',
                'text': 'Here\'s your pug!',
                'image_url': 'https://c2.staticflickr.com/%d/%s/%s_%s.jpg' % (farm, server, image_id, secret)
            }
        except:
            return {
                'fallback': 'Cute pugs everywhere',
                'title': 'Pugs everywhere!',
                'text': 'Here\'s your pug!',
                'image_url': 'https://c2.staticflickr.com/2/1681/24299810009_16fbc3a15c.jpg'
            }
    return message

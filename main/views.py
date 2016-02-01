import requests
from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import View
import json
import random

from main.models import Employee


class SlackBotView(View):

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(SlackBotView, self).dispatch(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = request.POST

        user = get_object_or_404(Employee, user__username=data['user_name'])

        token = "639f78bbda52d6edb7f18d52302ea7e6"
        company_id = '2'
        employee_id = user.employee_id

        clock_in_data = {
            'token': token,
            'company_id': company_id,
            'employee_id': employee_id
        }

        clock_in = requests.post('https://app.salarium.com/api/bundy/clock', clock_in_data)
        if json.loads(clock_in.content)['status'] == 0:
            token = self.get_account_token()
            clock_in_data = {
                'token': token,
                'company_id': company_id,
                'employee_id': employee_id
            }

            clock_in = requests.post('https://app.salarium.com/api/bundy/clock', clock_in_data)

        clock_in = json.loads(clock_in.content)
        status = 'in'
        if clock_in['time_out']:
            status = 'out'
        return JsonResponse({'text': '%s is logged %s' % (clock_in['employee_full_name'], status)})

    def get_account_token(self):
        user_data = {
            'email': 'ja@directworksmedia.com',
            'password': 'Ferower25'
        }

        response = requests.post('https://app.salarium.com/api/bundy_admin/register_device', user_data)
        response = json.loads(response.content)
        return response['account_token']


class JABotsView(View):

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(JABotsView, self).dispatch(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = request.POST
        keyword = ' '.join(data['text'].split(' ')[1:])
        if keyword == 'pug me' or 'pug' in keyword:
            response = requests.get('https://api.flickr.com/services/rest/?method=flickr.photos.search&api_key=515e81eaff9cb3f524806bc77b503ba3&text=dog%20pugs&format=json&nojsoncallback=1')
            response = json.loads(response.content)
            # random from 1 to 100
            index = random.randint(0, 99)
            owner = response['photos']['photo'][index]['owner']
            image_id = response['photos']['photo'][index]['id']
            message = 'https://www.flickr.com/photos/%s/%s' % (owner, image_id)

        return JsonResponse({'text': message})
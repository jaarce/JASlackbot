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
        return JsonResponse({'text': '%s is logged %s.' % (clock_in['employee_full_name'], status)})

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
        keyword = ' '.join(data['text'].split(' ')[0:])
        message = {'text': 'Hi!'}
        from plugins import food, pug, refresh, gif_translate

        message = pug.japlugin(keyword, message) if pug.japlugin(keyword, message) else message
        message = food.japlugin(keyword, message) if food.japlugin(keyword, message) else message
        message = refresh.japlugin(keyword, message) if refresh.japlugin(keyword, message) else message
        message = gif_translate.japlugin(keyword, message) if gif_translate.japlugin(keyword, message) else message

        return JsonResponse({
            'response_type': 'in_channel',
            'text': 'JA says',
            'attachments': [message]
        })


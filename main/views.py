import requests
from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import View
import json

from main.models import Employee


class SlackBotView(View):

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(SlackBotView, self).dispatch(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = request.POST

        user = get_object_or_404(Employee, user__username=data['user_name'])
        user_data = {
            'email': user.user.email,
            'password': user.salarium_password
        }

        return JsonResponse({'text': data['user_name']})

        response = requests.post('https://app.salarium.com/api/bundy_admin/register_device', user_data)
        response = json.loads(response.content)

        token = response['account_token']
        company_id = response['companies'][0]['company_id']
        employee_id = user.employee_id

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

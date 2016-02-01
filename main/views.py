from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import View


class SlackBotView(View):

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(SlackBotView, self).dispatch(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = request.POST

        return JsonResponse({'text': data['user_name']})

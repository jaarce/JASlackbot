from django.conf.urls import include, url
from django.contrib import admin

from main.views import SlackBotView

urlpatterns = [
    url(r'^log/$', SlackBotView.as_view()),
    url(r'^admin/', include(admin.site.urls)),
]

from django.urls import path

from django.contrib import admin
from polls.views import question_list, register_view

from django.urls import path

app_name = 'polls'

urlpatterns = [
    path('register', register_view, name='register'),
]
from django.urls import path

from django.contrib import admin
from polls.views import question_list

app_name = 'polls'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', question_list, name='question_list'),
]
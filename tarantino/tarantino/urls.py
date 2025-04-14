from django.urls import path

from django.contrib import admin
from polls.views import question_list

from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('polls.urls')),
    path('home', question_list, name='home')
]
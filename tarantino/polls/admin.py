from django.contrib import admin
from .models import Cinema, CinemaHall, Screening

@admin.register(Cinema)
class CinemaAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'contact_phone')
    search_fields = ('name', 'address')

@admin.register(CinemaHall)
class CinemaHallAdmin(admin.ModelAdmin):
    list_display = ('name', 'cinema', 'capacity')
    list_filter = ('cinema',)
    search_fields = ('name', 'cinema__name')

@admin.register(Screening)
class ScreeningAdmin(admin.ModelAdmin):
    list_display = ('movie', 'hall', 'start_time', 'price', 'duration')
    list_filter = ('hall__cinema', 'hall', 'start_time')
    search_fields = ('movie__title',)
    date_hierarchy = 'start_time'

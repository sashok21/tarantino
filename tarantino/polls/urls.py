from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    # Адміністратор
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin-dashboard/users/', views.admin_user_list, name='admin_user_list'),
    path('admin-dashboard/cinemas/', views.admin_cinema_list, name='admin_cinema_list'),
    path('admin-dashboard/halls/', views.admin_hall_list, name='admin_hall_list'),
    path('admin-dashboard/screenings/', views.admin_screening_list, name='admin_screening_list'),
    path('admin-dashboard/movies/', views.admin_movie_list, name='admin_movie_list'),
    path('admin-dashboard/tickets/', views.admin_ticket_list, name='admin_ticket_list'),

    # Зміни
    path('admin-dashboard/users/<int:user_id>/change/', views.admin_user_change, name='admin_user_change'),
    path('admin-dashboard/users/<int:user_id>/delete/confirm/', views.user_delete_confirm_view, name='admin_user_delete_confirm'),
    path('admin-dashboard/users/<int:user_id>/delete/', views.delete_user_view, name='admin_user_delete'),
    path('admin-dashboard/cinema/<int:pk>/change/', views.cinema_change_view, name='admin_main_cinema_change'),
    path('admin-dashboard/cinema/add/', views.cinema_add_view, name='admin_cinema_add'),
    path('admin-dashboard/cinema/<int:pk>/delete/', views.admin_cinema_delete, name='admin_main_cinema_delete'),

    path('admin-dashboard/hall/add/', views.hall_add_view, name='admin_hall_add'),
    path('admin-dashboard/halls/<int:pk>/change/', views.hall_change_view, name='admin_hall_change'),
    path('admin-dashboard/halls/<int:pk>/delete/', views.hall_delete_view, name='admin_hall_delete'),
    path('admin-dashboard/movies/add/', views.movie_add_view, name='admin_movie_add'),
    path('admin-dashboard/movies/<int:pk>/change/', views.movie_change_view, name='admin_movie_change'),
    path('admin-dashboard/movies/<int:pk>/delete/', views.movie_delete_view, name='admin_movie_delete'),
    path('admin-dashboard/movies/', views.admin_movie_list, name='admin_movie_list'),
    path('admin-dashboard/screening/add/', views.screening_add_view, name='admin_screening_add'),
    path('admin-dashboard/screening/<int:pk>/change/', views.screening_change_view, name='admin_screening_change'),
    path('admin-dashboard/screening/<int:pk>/delete/', views.screening_delete_view, name='admin_screening_delete'),
    path('screenings/<int:pk>/', views.screening_detail_view, name='screening_detail'),
    path('admin-dashboard/tickets/', views.admin_ticket_list, name='admin_ticket_list'),
    path('screenings/<int:screening_id>/purchase/', views.purchase_ticket_view, name='purchase_ticket'),
    path('ticket/success/', views.ticket_success_view, name='ticket_success'),
    path('purchase/<int:screening_id>/', views.purchase_ticket_view, name='purchase_ticket'),
    path('admin-dashboard/tickets/add/', views.admin_ticket_add, name='admin_ticket_add'),
    path('admin-dashboard/tickets/<int:pk>/change/', views.admin_ticket_change, name='admin_ticket_change'),
    path('admin-dashboard/tickets/<int:pk>/delete/', views.admin_ticket_delete, name='admin_ticket_delete'),
    path('tickets/<int:pk>/', views.ticket_detail_view, name='ticket_detail'),

    # Реєстрація
    path('register/', views.register_user, name='register'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),

    # Головні
    path('', views.home, name='home'),
    path('cinemas/', views.cinema_list, name='cinema_list'),
    path('cinemas/<int:cinema_id>/', views.cinema_detail, name='cinema_detail'),
    path('cinemas/<int:cinema_id>/halls/<int:hall_id>/', views.hall_detail, name='hall_detail'),
    path('my-tickets/', views.user_tickets, name='user_tickets'),
    path('screenings/today/', views.today_screenings, name='today_screenings'),

]

# Шлях до медіа файлів при розробці
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
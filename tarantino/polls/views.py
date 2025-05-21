from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils import timezone
from django.contrib import messages
from django.db.models import Prefetch
import random
import string
from django.contrib.admin.views.decorators import staff_member_required
from .models import Cinema, CinemaHall, Screening, Ticket, Movie
from .forms import CustomUserCreationForm, CustomAuthenticationForm, CinemaForm, CinemaHallForm, MovieForm, \
    ScreeningForm, TicketForm, TicketPurchaseForm, CustomUserChangeForm, AdminPasswordChangeForm


def home(request):
    """Головна сторінка з сьогоднішніми показами"""
    today = timezone.now().date()
    cinemas = Cinema.objects.all()
    today_screenings = Screening.objects.filter(
        start_time__date=today
    ).select_related('hall', 'hall__cinema')

    return render(request, 'cinema/home.html', {
        'cinemas': cinemas,
        'today_screenings': today_screenings,
    })


def cinema_list(request):
    """Список усіх кінотеатрів"""
    cinemas = Cinema.objects.all()
    return render(request, 'cinema/cinema_list.html', {'cinemas': cinemas})


def cinema_detail(request, cinema_id):
    """Детальна інформація про кінотеатр"""
    cinema = get_object_or_404(Cinema, pk=cinema_id)
    halls = cinema.halls.all()

    today = timezone.now().date()
    screenings = Screening.objects.filter(
        hall__cinema=cinema,
        start_time__date=today
    ).select_related('hall')

    return render(request, 'cinema/cinema_detail.html', {
        'cinema': cinema,
        'halls': halls,
        'screenings': screenings,
    })


def hall_detail(request, cinema_id, hall_id):
    """Детальна інформація про кінозал"""
    cinema = get_object_or_404(Cinema, pk=cinema_id)
    hall = get_object_or_404(CinemaHall, pk=hall_id, cinema=cinema)

    today = timezone.now().date()
    screenings = Screening.objects.filter(
        hall=hall,
        start_time__date=today
    ).select_related('hall')

    return render(request, 'cinema/hall_detail.html', {
        'cinema': cinema,
        'hall': hall,
        'screenings': screenings,
    })


def today_screenings(request):
    """Всі покази на сьогодні"""
    today = timezone.now().date()
    screenings = Screening.objects.filter(
        start_time__date=today
    ).select_related('hall', 'hall__cinema')

    return render(request, 'cinema/today_screenings.html', {
        'screenings': screenings,
        'date': today,
    })


def register_user(request):
    """Реєстрація користувача"""
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Реєстрація пройшла успішно!")
            return redirect('home')
        else:
            messages.error(request, "Реєстрація не вдалася. Будь ласка, виправте помилки.")
    else:
        form = CustomUserCreationForm()

    return render(request, 'cinema/register.html', {'form': form})


def login_user(request):
    """Вхід користувача"""
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Ласкаво просимо назад, {username}!")
                return redirect('home')
            else:
                messages.error(request, "Неправильне ім'я користувача або пароль.")
        else:
            messages.error(request, "Неправильне ім'я користувача або пароль.")
    else:
        form = CustomAuthenticationForm()

    return render(request, 'cinema/login.html', {'form': form})


def logout_user(request):
    """Вихід користувача"""
    logout(request)
    messages.success(request, "Ви успішно вийшли з системи!")
    return redirect('home')

@login_required
def user_tickets(request):
    # Отримуємо квитки, які належать поточному користувачу
    tickets = Ticket.objects.filter(user=request.user).order_by('-id')
    return render(request, 'cinema/user_tickets.html', {'tickets': tickets})

# Адміністраторські в'юшки

def staff_required(view_func):
    return user_passes_test(lambda u: u.is_staff)(view_func)


@staff_required
def admin_dashboard(request):
    return render(request, 'admin_dashboard.html')


@staff_required
def admin_user_list(request):
    users = User.objects.all()
    return render(request, 'dashboard/user_list.html', {'users': users})


@staff_required
def admin_cinema_list(request):
    cinemas = Cinema.objects.all()
    return render(request, 'dashboard/cinema_list.html', {'cinemas': cinemas})


@staff_required
def admin_hall_list(request):
    halls = CinemaHall.objects.all()
    return render(request, 'dashboard/hall_list.html', {'halls': halls})

@staff_required
def admin_movie_list(request):
    movies = Movie.objects.all()
    return render(request, 'dashboard/movie_list.html', {'movies': movies})

@staff_required
def screening_add_view(request):
    if request.method == 'POST':
        form = ScreeningForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin_screening_list')
    else:
        form = ScreeningForm()
    return render(request, 'dashboard/changes/screening_form.html', {'form': form, 'title': 'Додати сеанс'})

@staff_required
def screening_change_view(request, pk):
    screening = get_object_or_404(Screening, pk=pk)
    if request.method == 'POST':
        form = ScreeningForm(request.POST, instance=screening)
        if form.is_valid():
            form.save()
            return redirect('admin_screening_list')
    else:
        form = ScreeningForm(instance=screening)
    return render(request, 'dashboard/changes/screening_form.html', {'form': form, 'title': 'Редагувати сеанс'})

@staff_required
def screening_delete_view(request, pk):
    screening = get_object_or_404(Screening, pk=pk)
    if request.method == 'POST':
        screening.delete()
        return redirect('admin_screening_list')
    return render(request, 'dashboard/changes/screening_confirm_delete.html', {'screening': screening})

@staff_required
def admin_screening_list(request):
    screenings = Screening.objects.all()
    return render(request, 'dashboard/screening_list.html', {'screenings': screenings})


@staff_member_required
def admin_user_change(request, user_id):
    user_obj = get_object_or_404(User, pk=user_id)

    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=user_obj)
        pwd_form = AdminPasswordChangeForm(request.POST)

        if form.is_valid() and pwd_form.is_valid():
            form.save()
            if pwd_form.cleaned_data.get('password1'):
                pwd_form.save(user_obj)
                # Якщо адміністратор редагує не себе, оновлювати сесію не обов’язково
            return redirect('admin_user_list')  # або куди потрібно
    else:
        form = CustomUserChangeForm(instance=user_obj)
        pwd_form = AdminPasswordChangeForm()

    return render(request, 'dashboard/changes/user_change.html', {
        'form': form,
        'pwd_form': pwd_form,
        'user_obj': user_obj,
    })


@staff_required
def cinema_change_view(request, pk):
    cinema = get_object_or_404(Cinema, pk=pk)
    if request.method == 'POST':
        form = CinemaForm(request.POST, request.FILES, instance=cinema)
        if form.is_valid():
            form.save()
            return redirect('admin_cinema_list')
    else:
        form = CinemaForm(instance=cinema)
    return render(request, 'dashboard/changes/cinema_change.html', {'form': form, 'cinema': cinema})




@staff_required
def cinema_add_view(request):
    if request.method == 'POST':
        form = CinemaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin_cinema_list')
    else:
        form = CinemaForm()
    return render(request, 'dashboard/changes/cinema_add.html', {'form': form})

@staff_required
def hall_add_view(request):
    if request.method == 'POST':
        form = CinemaHallForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('admin_hall_list')
    else:
        form = CinemaHallForm()
    return render(request, 'dashboard/changes/hall_add.html', {'form': form})

@staff_required
def admin_ticket_list(request):
    tickets = Ticket.objects.select_related('user', 'screening__movie', 'screening__hall__cinema')
    return render(request, 'dashboard/ticket_list.html', {'tickets': tickets})

@staff_required
def admin_ticket_add(request):
    if request.method == 'POST':
        form = TicketForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin_ticket_list')
    else:
        form = TicketForm()

    return render(request, 'dashboard/changes/admin_ticket_form.html', {'form': form, 'title': 'Додати квиток'})

@staff_required
def admin_ticket_change(request, pk):
    ticket = get_object_or_404(Ticket, pk=pk)
    if request.method == 'POST':
        form = TicketForm(request.POST, instance=ticket)
        if form.is_valid():
            form.save()
            return redirect('admin_ticket_list')
    else:
        form = TicketForm(instance=ticket)
    return render(request, 'dashboard/changes/admin_ticket_form.html', {'form': form, 'title': 'Редагувати квиток'})

@staff_required
def admin_ticket_delete(request, pk):
    ticket = get_object_or_404(Ticket, pk=pk)
    if request.method == 'POST':
        ticket.delete()
        return redirect('admin_ticket_list')
    return render(request, 'dashboard/changes/admin_ticket_confirm_delete.html', {'ticket': ticket})

@staff_required
def hall_change_view(request, pk):
    hall = get_object_or_404(CinemaHall, pk=pk)

    if request.method == 'POST':
        form = CinemaHallForm(request.POST, request.FILES, instance=hall)
        if form.is_valid():
            form.save()
            return redirect('admin_hall_list')  # або куди хочеш після збереження
    else:
        form = CinemaHallForm(instance=hall)

    return render(request, 'dashboard/changes/hall_change.html', {'form': form, 'hall': hall})

@staff_required
def hall_delete_view(request, pk):
    hall = get_object_or_404(CinemaHall, pk=pk)
    if request.method == 'POST':
        hall.delete()
        return redirect('admin_hall_list')  # зміни на назву твоєї сторінки зі списком залів
    return render(request, 'dashboard/changes/hall_confirm_delete.html', {'hall': hall})

@staff_required
def movie_add_view(request):
    if request.method == 'POST':
        form = MovieForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('admin_movie_list')  # повертаємось до списку фільмів
    else:
        form = MovieForm()
    return render(request, 'dashboard/changes/movie_form.html', {'form': form, 'title': 'Додати фільм'})

@staff_required
def movie_change_view(request, pk):
    movie = get_object_or_404(Movie, pk=pk)
    if request.method == 'POST':
        form = MovieForm(request.POST, request.FILES, instance=movie)
        if form.is_valid():
            form.save()
            return redirect('admin_movie_list')
    else:
        form = MovieForm(instance=movie)
    return render(request, 'dashboard/changes/movie_form.html', {'form': form, 'title': 'Редагувати фільм'})

@staff_required
def movie_delete_view(request, pk):
    movie = get_object_or_404(Movie, pk=pk)
    if request.method == 'POST':
        movie.delete()
        return redirect('admin_movie_list')
    return render(request, 'dashboard/changes/movie_confirm_delete.html', {'movie': movie})
def ticket_detail_view(request, pk):
    ticket = get_object_or_404(Ticket, pk=pk)
    return render(request, 'cinema/ticket_detail.html', {'ticket': ticket})


def screening_detail_view(request, pk):
    screening = get_object_or_404(Screening, pk=pk)
    return render(request, 'cinema/screening_detail.html', {'screening': screening})

@login_required
def purchase_ticket_view(request, screening_id):
    screening = get_object_or_404(Screening, id=screening_id)

    if request.method == 'POST':
        form = TicketForm(request.POST, screening=screening)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.screening = screening
            ticket.user = request.user
            ticket.save()
            return redirect('ticket_success')  # Переконайся, що цей URL існує
    else:
        form = TicketForm(screening=screening)

    return render(request, 'cinema/purchase_ticket.html', {
        'screening': screening,
        'form': form
    })

def ticket_success_view(request):
    return render(request, 'cinema/ticket_success.html')



@staff_required
def delete_user_view(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        user.delete()
        return redirect('admin_user_list')
    return redirect('admin_user_delete_confirm', user_id=user_id)

@staff_required
def user_delete_confirm_view(request, user_id):
    user = get_object_or_404(User, id=user_id)
    return render(request, 'dashboard/changes/user_delete_confirm.html', {'user': user})

@staff_required
def admin_cinema_delete(request, pk):
    cinema = get_object_or_404(Cinema, pk=pk)
    if request.method == 'POST':
        cinema.delete()
        return redirect('admin_cinema_list')  # або інший URL з переліком кінотеатрів
    return render(request, 'dashboard/changes/cinema_confirm_delete.html', {'cinema': cinema})
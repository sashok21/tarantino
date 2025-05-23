from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from .models import Cinema, CinemaHall, Movie, Screening, Ticket


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, label='Електронна пошта')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
        labels = {
            'username': 'Імʼя користувача',
            'password1': 'Пароль',
            'password2': 'Підтвердження пароля',
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

class AdminPasswordChangeForm(forms.Form):
    password1 = forms.CharField(
        label="Новий пароль",
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password', 'class': 'form-control'}),
    )
    password2 = forms.CharField(
        label="Підтвердження пароля",
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password', 'class': 'form-control'}),
    )

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise ValidationError("Паролі не співпадають.")
        return cleaned_data

    def save(self, user):
        password = self.cleaned_data["password1"]
        user.set_password(password)
        user.save()

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(
        label='Імʼя користувача',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    password = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )

class CustomUserChangeForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
        labels = {
            'username': 'Імʼя користувача',
            'first_name': 'Імʼя',
            'last_name': 'Прізвище',
            'email': 'Електронна пошта',
        }
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }


class CinemaForm(forms.ModelForm):
    class Meta:
        model = Cinema
        fields = '__all__'

class CinemaHallForm(forms.ModelForm):
    class Meta:
        model = CinemaHall
        fields = ['cinema', 'name', 'capacity', 'description', 'image']


class MovieForm(forms.ModelForm):
    class Meta:
        model = Movie
        fields = ['title', 'description', 'duration', 'director', 'poster']

class ScreeningForm(forms.ModelForm):
    class Meta:
        model = Screening
        fields = '__all__'
        labels = {
            'movie': 'Фільм',
            'hall': 'Зал',
            'start_time': 'Час початку',
            'price': 'Ціна',
            'duration': 'Тривалість (хвилин)',
        }
        widgets = {
            'start_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['seat_number']
        labels = {'seat_number': 'Номер місця'}

    def __init__(self, *args, **kwargs):
        self.screening = kwargs.pop('screening', None)
        super().__init__(*args, **kwargs)

    def clean_seat_number(self):
        seat_number = self.cleaned_data['seat_number']
        screening = self.screening
        if not screening:
            raise forms.ValidationError('Сеанс не вказано.')

        capacity = screening.hall.capacity
        if seat_number < 1 or seat_number > capacity:
            raise forms.ValidationError(f"Номер місця повинен бути від 1 до {capacity}.")

        if Ticket.objects.filter(screening=screening, seat_number=seat_number).exists():
            raise forms.ValidationError("Це місце вже зайняте.")

        return seat_number


class TicketPurchaseForm(forms.Form):
    seat_number = forms.IntegerField(
        label='Номер місця',
        help_text='Введіть номер місця, яке бажаєте забронювати.'
    )

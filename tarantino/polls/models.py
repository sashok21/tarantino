from django.db import models
from django.contrib.auth.models import User

class Cinema(models.Model):
    name = models.CharField("Назва", max_length=200)
    address = models.CharField("Адреса", max_length=255)
    description = models.TextField("Опис")
    contact_phone = models.CharField("Контактний телефон", max_length=20)
    email = models.EmailField("Електронна пошта")
    opening_hours = models.CharField("Години роботи", max_length=255, help_text="наприклад, 10:00-22:00")
    image = models.ImageField("Зображення", upload_to='cinema_images/', null=True, blank=True)

    class Meta:
        verbose_name = "Кінотеатр"
        verbose_name_plural = "Кінотеатри"

    def __str__(self):
        return self.name



class CinemaHall(models.Model):
    cinema = models.ForeignKey(Cinema, on_delete=models.CASCADE, related_name='halls', verbose_name='Кінотеатр')
    name = models.CharField(max_length=100, verbose_name='Назва')
    capacity = models.PositiveIntegerField(verbose_name='Вмістимість')
    description = models.TextField(blank=True, verbose_name='Опис')
    image = models.ImageField(upload_to='hall_images/', null=True, blank=True, verbose_name='Зображення')

    class Meta:
        verbose_name = "Зал кінотеатру"
        verbose_name_plural = "Зали кінотеатрів"

    def __str__(self):
        return f"{self.cinema.name} - {self.name}"

class Movie(models.Model):
    title = models.CharField("Назва", max_length=200)
    description = models.TextField("Опис")
    duration = models.PositiveIntegerField("Тривалість у хвилинах", help_text="Тривалість у хвилинах")
    director = models.CharField("Режисер", max_length=100, blank=True)
    poster = models.ImageField("Постер", upload_to='movie_posters/', null=True, blank=True)

    class Meta:
        verbose_name = "Фільм"
        verbose_name_plural = "Фільми"

    def __str__(self):
        return self.title


from django.db.models import Count

class Screening(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='screenings')
    hall = models.ForeignKey(CinemaHall, on_delete=models.CASCADE, related_name='screenings')
    start_time = models.DateTimeField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    duration = models.PositiveIntegerField(help_text="Тривалість у хвилинах", default=90)

    class Meta:
        verbose_name = "Сеанс"
        verbose_name_plural = "Сеанси"

    def __str__(self):
        return f"{self.movie} - {self.hall.name} - {self.start_time.strftime('%Y-%m-%d %H:%M')}"

    @property
    def available_seats(self):
        total_seats = self.hall.capacity
        booked_seats = self.tickets.count()
        return total_seats - booked_seats


class Ticket(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tickets')
    screening = models.ForeignKey('Screening', on_delete=models.CASCADE, related_name='tickets')
    seat_number = models.PositiveIntegerField()
    purchase_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Квиток"
        verbose_name_plural = "Квитки"
        unique_together = ('screening', 'seat_number')  # Місце не може бути заброньоване двічі на один сеанс

    def __str__(self):
        return f"{self.user.username} - {self.screening.movie} - Місце {self.seat_number}"


from django.db import models
from django.conf import settings


class Profile(models.Model):
    genders = [("Male","Male"), ("Female", "Female")]
    user = models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    date_of_birth = models.DateField(blank=True, null=True)
    photo = models.ImageField(upload_to='users/%Y/%m/%d/', blank=True)
    gender = models.CharField(max_length=255, choices=genders, default="Male")

    def __str__(self):
        return f'Профиль пользователя {self.user.username}'
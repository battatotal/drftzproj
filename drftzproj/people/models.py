from django.db import models
from django.conf import settings
from PIL import ImageDraw, Image, ImageFont

from drftzproj.settings import BASE_DIR


class Profile(models.Model):
    genders = [("Male","Male"), ("Female", "Female")]
    user = models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    date_of_birth = models.DateField(blank=True, null=True)
    photo = models.ImageField(upload_to='users/%Y/%m/%d/', blank=True)
    gender = models.CharField(max_length=255, choices=genders, default="Male")
    liked = models.ManyToManyField('self', symmetrical=False, related_name='followers', blank=True)


    def __str__(self):
        return f'Профиль пользователя {self.user.username}'


    def save(self,*args, **kwargs):
        # добавляю водяной знак
        super().save(*args,**kwargs)
        newPhoto = Image.open(self.photo.path)
        if newPhoto.mode in ('RGBA', 'p'):
            newPhoto = newPhoto.convert("RGB")
        width, height = newPhoto.size
        draw = ImageDraw.Draw(newPhoto)
        image_text = "Watermark"
        font_size = int(width/15)
        font = ImageFont.truetype(f'{str(BASE_DIR)+"/watermark/Villa.ttf"}',font_size)
        x, y = int(width/2), int(height/2)
        draw.text((x,y), image_text, font=font, fill='#fff', stroke_width=5, stroke_fill='#222',anchor='ms')
        newPhoto.save(self.photo.path)

from django.template.backends import django
from rest_framework import serializers
from django.contrib.auth.models import User

from .models import Profile


class PeopleSerializer(serializers.ModelSerializer):
    #сериализатор профиля
    #скрытое поле
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Profile
        # fields = '__all__'
        fields = ('date_of_birth','photo','gender','user')



class UserSerializer(serializers.ModelSerializer):
    #Вложенный сериализатор
    class Meta:
        model = User
        fields = ('first_name','last_name',)



class PeopleListSerializer(serializers.ModelSerializer):
    #Сериализатор списка профилей


    user = UserSerializer()

    class Meta:
        model = Profile
        fields = "__all__"



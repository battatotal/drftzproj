import django.contrib.auth.models
from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import permissions
from .permissions import OnlyOneProfile

from .serializers import PeopleSerializer, PeopleListSerializer, UserSerializer
from .models import Profile
from .services import calc_dist

from django.core.mail import send_mail

from django_filters import rest_framework as filters
from django.http import HttpResponse



def mainview(request):
    #главная страница
    return HttpResponse("<h1>Админ-панель: admin/12345</h1>")



class DistFilter(filters.FilterSet):
    #Фильтр дистанции


    min_dist = filters.NumberFilter(field_name="distance", lookup_expr='lte')

    class Meta:
        model = Profile
        fields = ['min_dist', 'gender']




class PeopleApiView(generics.CreateAPIView):
    #создание и получение пользователя
    queryset = Profile.objects.all()
    serializer_class = PeopleSerializer
    permission_classes = (OnlyOneProfile,)



class PeopleApiList(generics.ListAPIView):
    #Возвращает список пользователей. Перегруженный метод get_queryset заполняет для пользователей поле
    #distance, для возможности фильтрации

    queryset = Profile.objects.all()
    serializer_class = PeopleListSerializer
    permission_classes = (permissions.IsAuthenticated,)
    filter_backends = [DjangoFilterBackend]
    filterset_class = DistFilter
    # filterset_fields = ["gender",]


    def get_queryset(self):
        #заполняю поле distance для каждого юзера кроме текущего
        current_user = Profile.objects.get(user_id=self.request.user.id)
        userlist = Profile.objects.exclude(user_id=current_user.id)
        for usr in userlist:
            dst = calc_dist(current_user.latitude, current_user.longitude, usr.latitude, usr.longitude)
            Profile.objects.filter(user_id=usr.user_id).update(distance=dst)

        #Возвращаю всех юзеров кроме текущего
        return Profile.objects.exclude(user_id=current_user.user_id)



class LikedApiView(APIView):
    #Позволяет ставить пользователю лайк, и если текущий пользователь уже в "лайках" у понравившегося пользователя
    #то пользователи получат мейлы друг друга

    def get(self, request, **kwargs):
        user_id = request.user.id
        profile = Profile.objects.get(user_id=user_id)
        currentUser = Profile.objects.get(user_id=user_id)
        resultUser = Profile.objects.get(user_id=kwargs['id'])
        profile.liked.add(resultUser)
        res = resultUser.liked.prefetch_related()
        if currentUser in res:
            #Отправка почт
            # subject = "Джанго"
            # forResultUser = f"Вы понравились {currentUser.user}! Почта участника: {currentUser.user.email}."
            # forCurrentUser = f"Вы понравились {resultUser.user}! Почта участника: {resultUser.user.email}."
            # send_mail(subject, forResultUser,'qweqw255eqwea@qweqweqweq.re', [resultUser])
            # send_mail(subject, forCurrentUser,'qweqw255eqwea@qweqweqweq.re',[currentUser])

            return Response({'Почта понравившегося участника': resultUser.user.email})

        return Response({'Вы поставили лайк': 'Если вы понравитесь этому участнику, вам придет его почта'})
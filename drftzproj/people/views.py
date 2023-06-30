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

from django.core.mail import send_mail

from django.contrib.auth.models import User
from django_filters import rest_framework as filters


# class UserFilter(filters.FilterSet):
#
#     class Meta:
#         model = User
#         fields = ['first_name', 'last_name']



class PeopleApiView(generics.CreateAPIView):
    queryset = Profile.objects.all()
    serializer_class = PeopleSerializer
    permission_classes = (OnlyOneProfile,)



class PeopleApiList(generics.ListAPIView):


    queryset = Profile.objects.all()
    serializer_class = PeopleListSerializer
    permission_classes = (permissions.IsAuthenticated,)
    filter_backends = [DjangoFilterBackend]
    # filterset_class = UserFilter
    filterset_fields = ["gender",]

    def get_queryset(self):
        #чтобы отображать всех пользователей кроме текущего
        user = self.request.user
        return Profile.objects.exclude(user_id=user)



class LikedApiView(APIView):

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
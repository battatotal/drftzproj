from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import permissions
from .permissions import OnlyOneProfile

from .serializers import PeopleSerializer
from .models import Profile

from django.core.mail import send_mail


class PeopleApiView(generics.CreateAPIView):
    queryset = Profile.objects.all()
    serializer_class = PeopleSerializer
    permission_classes = (OnlyOneProfile,)




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
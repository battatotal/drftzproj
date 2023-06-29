from django.shortcuts import render
from rest_framework import generics
from .permissions import OnlyOneProfile

from .serializers import PeopleSerializer
from .models import Profile


class PeopleApiView(generics.CreateAPIView):
    queryset = Profile.objects.all()
    serializer_class = PeopleSerializer
    permission_classes = (OnlyOneProfile,)
from django.contrib import admin
from django.urls import path, include
from people.views import PeopleApiView, LikedApiView, PeopleApiList

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/clients/drf-auth/', include('rest_framework.urls')),
    #path('people/', include('people.urls')),
    path('api/clients/create/', PeopleApiView.as_view()),
    path('api/clients/create/<int:pk>/', PeopleApiView.as_view()),
    path('api/clients/<int:id>/match/', LikedApiView.as_view()),
    path('api/list/', PeopleApiList.as_view()),
]


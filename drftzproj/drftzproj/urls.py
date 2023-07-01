from django.contrib import admin
from django.urls import path, include
from people.views import PeopleApiView, LikedApiView, PeopleApiList, mainview
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    path('', mainview, name="main"),
    path('admin/', admin.site.urls),
    path('api/clients/drf-auth/', include('rest_framework.urls')),
    #path('people/', include('people.urls')),
    path('api/clients/create/', PeopleApiView.as_view()),
    path('api/clients/create/<int:pk>/', PeopleApiView.as_view()),
    path('api/clients/<int:id>/match/', LikedApiView.as_view()),
    path('api/list/', PeopleApiList.as_view()),
]


urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

from rest_framework import serializers
from .models import Profile


class PeopleSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Profile
        # fields = '__all__'
        fields = ('date_of_birth','photo','gender','user')


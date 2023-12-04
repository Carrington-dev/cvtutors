from dataclasses import fields
from my_auth.models import NewUser, Profile
from rest_framework.serializers import ModelSerializer

from rest_framework import routers, serializers, viewsets

# Serializers define the API representation.
class NewUserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = NewUser
        fields = [
            'country', 'email', 'username', 'first_name', 'last_name', 'phone', 'disability', 'is_teacher', 'is_student'
        ]
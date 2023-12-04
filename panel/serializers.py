from dataclasses import fields
from panel.models import Course
from rest_framework.serializers import ModelSerializer

from rest_framework import routers, serializers, viewsets

# Serializers define the API representation.
class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields =  "__all__"
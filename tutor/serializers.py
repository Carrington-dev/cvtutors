from dataclasses import fields
from tutor.models import Subjects
from rest_framework.serializers import ModelSerializer

from rest_framework import routers, serializers, viewsets

# Serializers define the API representation.
class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subjects
        fields =  ["id", "name"]
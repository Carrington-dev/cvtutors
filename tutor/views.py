from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from tutor.models import Subjects
from tutor.serializers import SubjectSerializer


class SubjectViewSet(viewsets.ModelViewSet):
    queryset = Subjects.objects.all()
    serializer_class = SubjectSerializer

    def get(self, request):
        serializer = SubjectSerializer(self.queryset)
        return Response(serializer.data)

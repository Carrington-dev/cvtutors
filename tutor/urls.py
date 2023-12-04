from django.urls import path

from panel.serializers import PostSerializer
from . import views as panel_views
from rest_framework import routers
from django.contrib.auth import views as auth_views

router = routers.DefaultRouter()
router.register("subjects", panel_views.SubjectViewSet, basename="subject")

urlpatterns = [
    # 
]

urlpatterns += router.urls
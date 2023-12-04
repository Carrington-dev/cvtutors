from django.urls import path

from panel.serializers import PostSerializer
from . import views as panel_views
from rest_framework import routers
from django.contrib.auth import views as auth_views

router = routers.DefaultRouter()
router.register("homeworks", panel_views.CourseViewSet, basename="homework")

urlpatterns = [
    path("user-info/", panel_views.apply1, name='apply1'),
    path("user-info-2/", panel_views.apply2, name='apply2'),
    path("user-info-3/", panel_views.apply3, name='apply3'),
    path("pricing/", panel_views.pricing, name='pricing'),
    path("cities_json/", panel_views.cities_json, name='cities_json'),
]

urlpatterns += router.urls
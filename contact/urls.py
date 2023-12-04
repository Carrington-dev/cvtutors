from django.urls import include, path
from rest_framework.routers import DefaultRouter
from contact import views as contact_views 

router = DefaultRouter()
router.register(r'contacts', contact_views.ContactViewSet, basename='contactss')

urlpatterns = [
    # path('api/', include(router.urls)),
    path("", contact_views.contact, name="contact"),
    path("subscribe/", contact_views.subcribe, name="subscribe"),
]

# urlpatterns += router.urls
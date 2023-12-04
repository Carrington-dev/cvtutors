from django.conf import settings
from django.contrib import admin
from django.shortcuts import render
from my_auth import views as my_auth
from django.urls import path, include
from panel.sitemaps import *
from learn.admin import worker_admin_site
from panel.feeds import LatestCoursesFeed
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap

admin.site.site_header = "Carrington Visionary Academy"
admin.site.site_title = "Carrington Visionary Academy Admin Portal"
admin.site.index_title = "Carrington Visionary Academy welcomes you!!!"
# worker_admin_site.site_header = "FlexyTuta"
# worker_admin_site.site_title = "FlexyTuta Admin Portal"
# worker_admin_site.index_title = "FlexyTuta welcomes you!!!"



sitemaps = {
 'courses': CourseSitemap,
 'static': StaticSitemap,
}

#handler404 = 'my_auth.handler404p'

urlpatterns = [
    path('grappelli/', include('grappelli.urls')), # grappelli URLS
    path('power/', admin.site.urls),
    path('tutors/', worker_admin_site.urls, name="tadmin"),
    #path('404-not-found/', my_auth.handler404p, name="handler404p"),
    path("", include("my_auth.urls")),
    path("contact/", include("contact.urls")),
    path("apply/", include("panel.urls")),
    path("cart/", include("cart.urls")),
    path("pay/", include("pay.urls")),
    path("learn/", include("learn.urls")),
    path("tutor/", include("tutor.urls")),
    # path("checkout/", include("cart.shop_urls")),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    path('feed/', LatestCoursesFeed(), name='course_feed'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
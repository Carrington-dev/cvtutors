from django.contrib.sitemaps import Sitemap
from panel.models import Course
from django.shortcuts import reverse

class CourseSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.9
    
    def items(self):
        return Course.objects.all().filter(status="published")
    
    def lastmod(self, obj):
        return obj.updated


class StaticSitemap(Sitemap):
    """Reverse 'static' views for XML sitemap."""
    changefreq = "daily"
    priority = 0.5

    def items(self):
        # Return list of url names for views to include in sitemap
        return ['home', 'about', 'pricing', 'contact', 'profile']

    def location(self, item):
        return reverse(item)
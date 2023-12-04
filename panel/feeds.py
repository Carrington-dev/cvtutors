from django.contrib.syndication.views import Feed
from django.template.defaultfilters import truncatewords
from django.urls import reverse_lazy
from panel.models import Course

class LatestCoursesFeed(Feed):
    title = 'FlexyTuta Courses'
    link = reverse_lazy('courses')
    description = 'New courses on FlexyTuta.'
    
    def items(self):
        return Course.objects.all().filter(status="published")[:5]
    
    def item_title(self, item):
        return item.name
    
    def item_description(self, item):
        return truncatewords(item.describe, 50)
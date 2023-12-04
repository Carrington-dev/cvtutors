from django.contrib import admin

from tutor.models import Subjects

@admin.register(Subjects)
class SubjectsAdmin(admin.ModelAdmin):
    '''Admin View for Subject'''

    list_display = ('name',)
    list_filter = ('name',)
    
    search_fields = ('name',)
    # date_hierarchy = ''
    ordering = ('name',)
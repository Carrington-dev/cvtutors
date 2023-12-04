from django.contrib import admin

from contact.models import Contact, Subscribe
from my_auth.admin import export_to_csv

# Register your models here.
@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    '''Admin View for Contact'''
    list_display = ('name', 'email', 'subject', 'phone', 'message', 'date_recieved', 'date_last_viewed')
    list_filter = ('name', 'email',)
    readonly_fields = ('message',)
    search_fields = ('name',)
    ordering = ('name',)

@admin.register(Subscribe)
class SubscribeAdmin(admin.ModelAdmin):
    '''Admin View for Subscribe'''

    list_display = ('email', 'is_subscribed', 'date_recieved', 'date_last_viewed')
    list_filter = ('is_subscribed',)
    search_fields = ('email', )
    date_hierarchy = 'date_recieved'
    ordering = ('-pk',)
    list_per_page: int = 30
    actions = [export_to_csv]
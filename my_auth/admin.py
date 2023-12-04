from django.contrib import admin

# Register your models here.
from my_auth.models import NewUser, Profile, Transaction
from contact.models import *
import csv
from django.core.mail import  send_mass_mail
import datetime
from django.http import HttpResponse
from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.utils.safestring import mark_safe


def make_tutor(modeladmin, request, queryset):
    # send_mass_mail()
    queryset.update(is_teacher=True)
    queryset.update(is_admin=True)
    queryset.update(is_staff=True)
    queryset.update(is_superuser=False)

def approve_tutor(modeladmin, request, queryset):
    queryset.update(occupation='Approved Tutor')

def put_on_probation(modeladmin, request, queryset):
    queryset.update(occupation='On Probation')

def make_applicant(modeladmin, request, queryset):
    queryset.update(occupation='Applicant Tutor')

def cancel_tutor(modeladmin, request, queryset):
    queryset.update(occupation='Cancelled')



def publish(self, request, queryset):
    queryset.update(status="published")

def mark_as_viewed(self, request, queryset):
    queryset.update(viewed=True)

mark_as_viewed.short_description = "Mark as read"

def export_to_csv(modeladmin, request, queryset):
    opts = modeladmin.model._meta
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; \
            filename={}.csv'.format(opts.verbose_name)
    writer = csv.writer(response)

    fields = [field for field in opts.get_fields() if not field.many_to_many and not field.one_to_many]
    writer.writerow([field.verbose_name for field in fields])

    for obj in queryset:
        data_row = []
        for field in fields:
            value = getattr(obj, field.name)
            if isinstance(value, datetime.datetime):
                value = value.strftime('%d/%m/%Y')
            data_row.append(value)
        writer.writerow(data_row)
    return response

export_to_csv.short_description = 'Export to CSV'

# Register your models here.
@admin.register(NewUser)
class NewUserAdmin(admin.ModelAdmin):
    '''Admin View for NewUser'''

    
    list_display = ('id','username','email', 'first_name','last_name','phone','country', 'is_teacher','is_active', 'is_staff','is_admin','is_superuser') 
    readonly_fields=('date_joined', 'last_login', 'password','username','email', 'is_active')
    actions = [make_tutor,]# export_to_csv]
    search_fields = ['email']

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    '''Admin View for Profile'''

    list_display = ('user','occupation','preview', 'last_name', 'first_name')
    list_filter = ('occupation',)
    ordering = ('user',)
    actions = [approve_tutor, put_on_probation, make_applicant, cancel_tutor, export_to_csv]

    @mark_safe
    def preview(self, obj):
        template = u"""<img src="{url}" style="max-height: {size};" />"""
        config = {
            'image_field': 'image',
            'image_size': '50px',
        }
        custom_config = getattr(self, 'fancy_preview', {})
        config.update(custom_config)
        image = getattr(obj, config['image_field'], None)
        url = image.url if image else ''
        return template.format(url=url, size=config['image_size'])
    preview.short_description=_('preview')
    preview.allow_tags = True

    def first_name(self, obj):
        return obj.user.first_name
    def last_name(self, obj):
        return obj.user.last_name

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    '''Admin View for Transaction'''

    list_display = ('amount', 'status')
    list_filter = ('status',)
    search_fields = ('user', 'status', )
    raw_id_fields = ['user']
    ordering = ('-pk',)
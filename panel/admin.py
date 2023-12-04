from learn.models import Module
from my_auth.admin import export_to_csv
from panel.models import *
from django.urls import reverse
from django.contrib import admin
from django.utils.safestring import mark_safe
from django.utils.html import mark_safe


class ModuleInline(admin.TabularInline):
    model = Module
    list_display = ('course', 'title', 'order', 'edit_module')
    extra = 0

    def edit_module(self, obj):
        display_text = "<a href={}>{}</a>".format(reverse('admin:{}_{}_change'.format(obj._meta.app_label, 
        obj._meta.model_name), args=(obj.pk,)), obj.name)
             
        if display_text:
            return mark_safe(display_text)
        return "-"

class OrderProductInline(admin.TabularInline):
    model = OrderProduct
    readonly_fields = ['order','payment','product','user','quantity', 'hours', 'is_ordered']
    extra = 0

    def hours(self, obj):
        return obj.quantity

class Feature(admin.TabularInline):
    model = ProductFeature
    list_display = ('name', 'price', 'created', 'updated')
    list_filter = ('name',)
    search_fields = ('name',)
    date_hierarchy = 'created'
    ordering = ('-pk',)
    extra = 0

    

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    '''Admin View for Order'''

    list_display = ['pk', "email", "first_name", "last_name", "country", "payment_id",'order_pdf','get_order_total', "is_ordered", 'date_ordered','last_viewed']
    list_filter = ('country',)
    inlines = [OrderProductInline]
    search_fields = ('email',)
    date_hierarchy = 'date_ordered'
    ordering = ('-pk',)
    list_per_page: int = 30

    def payment_id(self, obj):
        if obj.payment is not None:
            return obj.payment.payment_id
        return "No payment found"

    def get_order_total(self, obj):
        return obj.get_order_total()

    
    
    def order_pdf(self, obj):
        url = reverse('admin_order_detail', args=[obj.id])
        return mark_safe(f'<a href="{url}">Reciept</a>')
    
    order_pdf.short_description = 'Invoice'
    get_order_total.short_description = 'Total'

@admin.register(Category)
class CategorysAdmin(admin.ModelAdmin):
    '''Admin View for Category'''

    list_display = ('name',)
    search_fields = ('name',)
    ordering = ('-pk',)


def publish(self, request, queryset):
    queryset.update(status="published")



@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    '''Admin View for Course'''

    list_display = ('name', 'category', 'description','image_view','status','total_modules',)
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}
    inlines = [ModuleInline]
    ordering = ('-pk',)
    actions = [publish]
    list_per_page: int = 20
    actions = [export_to_csv]

    def description(self, obj):
        txt = obj.describe[:30] if obj.describe is not None else "Describe me"
        return txt

    def category(self, obj):
        return obj.category.name
    
    # @property
    def image_view(self, obj):
        if obj.image:
            return mark_safe('<img src="{}" width="200" height="133.25" />'.format(obj.image.url))
        return ""
    
    
    
    def total_modules(self, obj):
            return obj.modules.count()
    
    # @mark_safe
    # def image_view(self, obj):
    #     a = f"<a href='{obj.image.url}'><img src='{obj.image.url}' /></a>"

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    '''Admin View for Product'''

    list_display = ('name', 'price', 'hours', 'product_type','product','status', 'created', 'updated', 'is_advanced')
    list_filter = ('name',)
    readonly_fields = ('created',)
    search_fields = ('name',)
    date_hierarchy = 'created'
    ordering = ('-pk',)
    inlines = [ Feature ]

    def product(self, obj):
        if obj.product is  None:
            return "Primary Product"
        else:
            return str(self.obj.name)
        


@admin.register(ProductFeature)
class ProductFeatureAdmin(admin.ModelAdmin):
    '''Admin View for ProductFeature'''

    list_display = ('name', 'price', 'created', 'updated')
    list_filter = ('name',)
    search_fields = ('name',)
    date_hierarchy = 'created'
    ordering = ('-pk',)
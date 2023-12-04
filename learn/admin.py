from django.contrib import admin
from django.contrib import messages
from django.utils.html import mark_safe
from .models import *



# @admin.register(Subject)
# class SubjectAdmin(admin.ModelAdmin):
#     list_display = ['title', 'slug']
#     prepopulated_fields = {'slug': ('title',)}
@admin.register(Content)
class ContentAdmin(admin.ModelAdmin):
    '''Admin View for Content '''

    list_display = ('module', 'content_type', 'object_id', 'item', 'order')
    
    ordering = ('pk',)

@admin.register(Text)
class TextAdmin(admin.ModelAdmin):
    '''Admin View for Text'''

    pass

class TextInline(admin.TabularInline):
    model = Text
    fields = ['owner','module', 'title', 'content',]
    extra: int = 0

    def save_model(self, request, obj, form, change):
        obj.trainer = request.user
        super().save_model(request, obj, form, change)

class VideoInline(admin.TabularInline):
    model = Video
    fields = ['owner','module', 'title',  'url',]
    extra: int = 0
    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        super().save_model(request, obj, form, change)

class EyeInline(admin.TabularInline):
    model = Eye
    fields = ['owner','module', 'title',  'file',]
    extra: int = 0
    
    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        super().save_model(request, obj, form, change)

class FileInline(admin.TabularInline):
    model = File
    fields = ['owner', 'module', 'title',  'file',]
    extra: int = 0
    
    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        super().save_model(request, obj, form, change)

class ImageInline(admin.TabularInline):
    model = Image
    fields = ['owner', 'module', 'title',  'file',]
    extra: int = 0
    
    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        super().save_model(request, obj, form, change)


class ModuleInline(admin.StackedInline):
    model = Module
    list_display = ('course', 'title', 'order', 'edit_module')
    extra = 1

    def edit_module(self, obj):
        display_text = "<a href={}>{}</a>".format(reverse('admin:{}_{}_change'.format(obj._meta.app_label, 
        obj._meta.model_name), args=(obj.pk,)), obj.name)
             
        if display_text:
            return mark_safe(display_text)
        return "-"


    # order_by = ['order']


class WorkerAdmin(admin.AdminSite):
    site_header = "FlexyTuta Pty Ltd"
    site_title = "FlexyTuta Admin Portal"
    index_title = "FlexyTuta welcomes you!!!"

worker_admin_site = WorkerAdmin(name='worker_admin')

@admin.register(Module, site=worker_admin_site)
class ModuleAdmin(admin.ModelAdmin):
    list_display = ('course', 'title', 'order')
    inlines = [TextInline,
                VideoInline,
                EyeInline,
                FileInline,
                ImageInline
            ]
    extra = 0
    # def videos_display(self, obj):
    #     display_text = ", ".join([
    #         "<a href={}>{}</a>".format(
    #                 reverse('admin:{}_{}_change'.format(obj._meta.app_label, obj._meta.model_name),
    #                 args=(child.pk,)),
    #             child.name)
    #          for child in obj.videos.all()
    #     ])
    #     if display_text:
    #         return mark_safe(display_text)
    #     return "-"
# worker_admin_site.register(Subscribe)
# worker_admin_site.register(Account, AccountAdmin)


def publish(self, request, queryset):
    queryset.update(status="published")

@admin.register(Course, site=worker_admin_site)
class CourseAdmin(admin.ModelAdmin):
    '''Admin View for Course'''

    list_display = ('name', 'category', 'image_view','course_view','status','students', 'likes_by', 'graduated', 'module_display')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}
    ordering = ('-pk',)
    list_per_page = 20
    # readonly_fields = ['slug']
    inlines = [ ModuleInline ]
    actions = [publish]
    exclude = ['trainer','students_graduated', 'students_enrolled', 'student_likes', 'publish']

    def students(self, obj):
        return obj.students_enrolled.count()

    def graduated(self, obj):
        return obj.students_completed.count()

    def likes_by(self, obj):
        return obj.student_likes.count()

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(trainer=request.user)

    def save_model(self, request, obj, form, change):
        obj.trainer = request.user
        super().save_model(request, obj, form, change)


    def module_display(self, obj):
        background = """
            background-color: #4CAF50; /* Green */
            border: none;
            color: white;
            padding: 15px 32px;
            text-align: center;
            text-decoration: none;
            display: inline-block;
            font-size: 16px;"""
        display_text = ", ".join([
            "<a style={} grp-content-title' href={}>{}</a><br/>".format(background,
                    reverse('worker_admin:{}_{}_change'.format(child._meta.app_label, child._meta.model_name),
                    args=(child.pk,)),
                child.title)
             for child in obj.modules.all()
        ])
        if display_text:
            return mark_safe(display_text)
        return "-"

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

    def course_view(self, obj):
        return mark_safe('<a href="{}" width="200" height="133.25" >View course</a>'.format(obj.get_absolute_url))
    
    image_view.short_description= ('preview')
    image_view.allow_tags = True
    
    
    # def has_change_permission(self, request, obj=None):
    #     has_class_permission = super(CourseAdmin, self).has_change_permission(request, obj)

    #     if not has_class_permission:
    #         return False
    #     if obj is None:
    #         return True
    #     if obj is not None and not request.user.is_superuser and request.user.id != obj.trianer.id:
    #         messages.add_message(request, messages.INFO, 'You do not have any access permission to this modules')
    #         return False
    
@admin.register(Content, site=worker_admin_site)
class ContentAdmin(admin.ModelAdmin):
    '''Admin View for Content '''

    list_display = ('module', 'content_type', 'object_id', 'item', 'order')
    
    ordering = ('pk',)
    list_per_page = 20

@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = ('course', 'title', 'description', 'order')
    inlines = [TextInline,
                VideoInline,
                EyeInline,
                FileInline,
                ImageInline
            ]
    # list_filter = ['created', 'subject']
    # search_fields = ['title', 'overview']
    # prepopulated_fields = {'slug': ('title',)}
    
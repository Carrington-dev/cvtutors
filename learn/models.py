from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.urls import reverse
from learn.fields import OrderField
from flexyweb import settings
from panel.models import Course
# from PIL import Image
import PIL.Image
# Create your models here.
class Module(models.Model):
    course = models.ForeignKey(Course,
                               related_name='modules',
                               on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    order = OrderField(blank=True, for_fields=['course'])
    image = models.ImageField(default='modules/default.png', upload_to='modules/thumbnails', help_text='Make it a little bit bigger for cropping')
    students_completed = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='modules_completed', blank=True)
    
    class Meta:
        ordering = ['order']

    def __str__(self):
        return f'{self.order}. {self.title}'
    
    def is_user_in(self, request):
        if request.user in self.students_completed:
            return True
        return False
    
    def get_absolute_url(self):
        return reverse('course', 
            args=[self.course.publish.year,
            self.course.publish.month,
            self.course.publish.day,
            self.course.slug, self.pk])

    def save(self, *args, **kwargs):  # new
        super().save()
        img = PIL.Image.open(self.image.path)
        w, h = img.size
       
        if w < 400 or h < 400:
            del img
            self.image = "modules/default.png"
        else:
            img.thumbnail((400, 400))
            img.save(f"{self.image.path}")
        return super().save(*args, **kwargs)
    # def get_absolute_url(self):
    #     return reverse('module', args=[self.course.id, self.pk])



class Content(models.Model):
    module = models.ForeignKey(Module,
                               related_name='contents',
                               on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType,
                                     on_delete=models.CASCADE,
                                     limit_choices_to={'model__in':(
                                     'text',
                                     'video',
                                     'image',
                                     'eye',
                                     'file')})
    object_id = models.PositiveIntegerField()
    item = GenericForeignKey('content_type', 'object_id')
    order = OrderField(blank=True, for_fields=['module'])

    class Meta:
        ordering = ['order']


class ItemBase(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL,
                              related_name='%(class)s_related',
                              on_delete=models.CASCADE)
    module = models.ForeignKey(Module,
                               related_name='%(class)s_contents',
                               on_delete=models.CASCADE, default=2)
    title = models.CharField(max_length=250)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.title


class Text(ItemBase):
    students_completed = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='text_completed', blank=True)
    content = models.TextField()


class File(ItemBase):
    students_completed = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='file_completed', blank=True)
    file = models.FileField(upload_to='modules/files')


class Image(ItemBase):
    students_completed = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='image_completed', blank=True)
    file = models.FileField(upload_to='modules/images')


class Video(ItemBase):
    students_completed = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='video_completed', blank=True)
    url = models.URLField()

class Eye(ItemBase):
    students_completed = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='eye_completed', blank=True)
    file = models.FileField(upload_to='modules/videos')
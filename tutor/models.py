from django.db import models

from flexyweb import settings

# Create your models here.
class Subjects(models.Model):
    name = models.CharField(max_length=50, unique=True)
    tutors = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="subjects", blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Subjects'
        verbose_name_plural = 'Subjectss'
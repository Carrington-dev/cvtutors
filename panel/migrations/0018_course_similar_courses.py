# Generated by Django 4.0 on 2022-12-01 17:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('panel', '0017_rename_students_joined_course_students_completed'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='similar_courses',
            field=models.ManyToManyField(blank=True, related_name='similar', to='panel.Course'),
        ),
    ]
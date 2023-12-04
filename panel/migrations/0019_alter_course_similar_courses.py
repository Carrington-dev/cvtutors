# Generated by Django 4.0 on 2022-12-02 08:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('panel', '0018_course_similar_courses'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='similar_courses',
            field=models.ManyToManyField(blank=True, help_text='Enter all your courses to recommend', to='panel.Course'),
        ),
    ]
# Generated by Django 4.0 on 2022-11-13 13:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('panel', '0006_course_students_enrolled'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='motivation',
            field=models.CharField(blank=True, help_text='Increase your skills in this course', max_length=500, null=True),
        ),
    ]

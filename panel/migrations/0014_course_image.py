# Generated by Django 4.0 on 2022-11-30 10:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('panel', '0013_alter_course_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='image',
            field=models.ImageField(default='default.jpg', upload_to='profile_pics'),
        ),
    ]

# Generated by Django 4.0 on 2022-12-14 11:40

from django.db import migrations
import django_resized.forms


class Migration(migrations.Migration):

    dependencies = [
        ('my_auth', '0007_alter_newuser_is_active'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='image',
            field=django_resized.forms.ResizedImageField(crop=['middle', 'center'], default='profile_pics/default.png', force_format='JPEG', keep_meta=True, quality=75, scale=0.5, size=[300, 300], upload_to='profile_pics'),
        ),
    ]

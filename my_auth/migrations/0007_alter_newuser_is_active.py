# Generated by Django 4.0 on 2022-12-14 10:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_auth', '0006_alter_newuser_first_name_alter_newuser_is_active_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='newuser',
            name='is_active',
            field=models.BooleanField(default=True, verbose_name='active'),
        ),
    ]

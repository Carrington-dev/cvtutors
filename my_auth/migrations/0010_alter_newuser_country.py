# Generated by Django 4.0 on 2023-01-02 14:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_auth', '0009_alter_newuser_country'),
    ]

    operations = [
        migrations.AlterField(
            model_name='newuser',
            name='country',
            field=models.CharField(default='South Africa', max_length=500, verbose_name='country'),
        ),
    ]
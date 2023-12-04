# Generated by Django 4.0 on 2022-11-13 13:03

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=200)),
                ('email', models.EmailField(blank=True, max_length=200)),
                ('subject', models.CharField(blank=True, max_length=200)),
                ('phone', models.CharField(blank=True, max_length=20)),
                ('message', models.TextField(blank=True)),
                ('date_recieved', models.DateTimeField(auto_now_add=True)),
                ('date_last_viewed', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Contact',
                'verbose_name_plural': 'Contacts',
            },
        ),
        migrations.CreateModel(
            name='Subscribe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=200, null=True)),
                ('email', models.EmailField(max_length=200)),
                ('is_subscribed', models.BooleanField(default=True)),
                ('date_recieved', models.DateTimeField(auto_now_add=True)),
                ('date_last_viewed', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Subscribe',
                'verbose_name_plural': 'Subscribe',
            },
        ),
    ]

# Generated by Django 4.0 on 2022-11-13 13:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('panel', '0003_course_trainer'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
    ]

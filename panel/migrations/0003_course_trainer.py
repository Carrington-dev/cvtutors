# Generated by Django 4.0 on 2022-11-13 13:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('my_auth', '0002_alter_profile_specialty'),
        ('panel', '0002_product_course'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='trainer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='my_auth.newuser'),
        ),
    ]

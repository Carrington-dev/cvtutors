# Generated by Django 4.0 on 2023-01-02 14:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('panel', '0022_alter_order_phone'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='country',
            field=models.CharField(default='South Africa', max_length=600),
        ),
    ]

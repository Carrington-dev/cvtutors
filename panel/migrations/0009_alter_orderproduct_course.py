# Generated by Django 4.0 on 2022-11-14 11:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('panel', '0008_orderproduct_course_alter_orderproduct_product'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderproduct',
            name='course',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='order_items', to='panel.course'),
        ),
    ]

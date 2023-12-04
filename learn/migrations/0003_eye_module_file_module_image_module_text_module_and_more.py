# Generated by Django 4.0 on 2022-12-02 08:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('learn', '0002_module_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='eye',
            name='module',
            field=models.ForeignKey(default=2, on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s_contents', to='learn.module'),
        ),
        migrations.AddField(
            model_name='file',
            name='module',
            field=models.ForeignKey(default=2, on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s_contents', to='learn.module'),
        ),
        migrations.AddField(
            model_name='image',
            name='module',
            field=models.ForeignKey(default=2, on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s_contents', to='learn.module'),
        ),
        migrations.AddField(
            model_name='text',
            name='module',
            field=models.ForeignKey(default=2, on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s_contents', to='learn.module'),
        ),
        migrations.AddField(
            model_name='video',
            name='module',
            field=models.ForeignKey(default=2, on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s_contents', to='learn.module'),
        ),
    ]
# Generated by Django 4.2.14 on 2024-09-07 09:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ams', '0008_alter_bundle_container'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bundle',
            name='element',
        ),
        migrations.RemoveField(
            model_name='bundle',
            name='step',
        ),
    ]

# Generated by Django 4.2.14 on 2024-10-14 11:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_alter_bundletype_created_by_and_more'),
        ('ams', '0011_alter_bundle_created_by_alter_bundle_modified_by_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='bundle',
            name='step',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.step'),
        ),
    ]

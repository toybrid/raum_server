# Generated by Django 4.2.14 on 2024-09-07 08:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0003_bundletype'),
        ('ams', '0004_rename_uri_product_slug'),
    ]

    operations = [
        migrations.CreateModel(
            name='Bundle',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('active', models.BooleanField(default=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('version', models.IntegerField(blank=True, default=0, null=True)),
                ('slug', models.CharField(blank=True, editable=False, max_length=4096, null=True, unique=True)),
                ('approved_at', models.DateTimeField(blank=True, editable=False, null=True)),
                ('approved_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('bundle_type', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.bundletype')),
                ('container', models.OneToOneField(editable=False, on_delete=django.db.models.deletion.CASCADE, to='ams.container')),
                ('created_by', models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(class)s_created_by', to=settings.AUTH_USER_MODEL)),
                ('element', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.element')),
                ('modified_by', models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(class)s_modified_by', to=settings.AUTH_USER_MODEL)),
                ('status', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.status')),
                ('step', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.step')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
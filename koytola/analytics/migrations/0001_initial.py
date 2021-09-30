# Generated by Django 3.1 on 2021-08-26 12:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import koytola.core.utils.json_serializer


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('profile', '0001_initial'),
        ('product', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tracking',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('private_metadata', models.JSONField(blank=True, default=dict, encoder=koytola.core.utils.json_serializer.CustomJsonEncoder, null=True)),
                ('metadata', models.JSONField(blank=True, default=dict, encoder=koytola.core.utils.json_serializer.CustomJsonEncoder, null=True)),
                ('date', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('type', models.CharField(choices=[('OTHER', 'other'), ('CATEGORY', 'category'), ('COMPANY', 'company'), ('PRODUCT', 'product')], default='other', max_length=255)),
                ('ip', models.CharField(blank=True, max_length=255)),
                ('country', models.CharField(blank=True, max_length=255)),
                ('region', models.CharField(blank=True, max_length=255)),
                ('city', models.CharField(blank=True, max_length=255)),
                ('postal', models.CharField(blank=True, max_length=255)),
                ('location_details', models.JSONField(blank=True, default=dict, encoder=koytola.core.utils.json_serializer.CustomJsonEncoder)),
                ('referrer', models.CharField(blank=True, max_length=255)),
                ('device_type', models.CharField(blank=True, max_length=255)),
                ('device', models.CharField(blank=True, max_length=30)),
                ('browser', models.CharField(blank=True, max_length=30)),
                ('system', models.CharField(blank=True, max_length=30)),
                ('system_version', models.CharField(blank=True, max_length=30)),
                ('parameters', models.JSONField(blank=True, default=dict, encoder=koytola.core.utils.json_serializer.CustomJsonEncoder)),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='product.category')),
                ('company', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='profile.company')),
                ('product', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='product.product')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='analytics', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-date'],
                'permissions': (('manage_tracking', 'Manage tracking.'),),
            },
        ),
    ]

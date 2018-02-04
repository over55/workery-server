# Generated by Django 2.0 on 2018-02-04 04:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shared_foundation', '0001_initial'),
        ('tenant_foundation', '0009_auto_20180204_0427'),
    ]

    operations = [
        migrations.AddField(
            model_name='customercomment',
            name='created_by',
            field=models.ForeignKey(default=1, help_text='The user whom created this object.', on_delete=django.db.models.deletion.CASCADE, related_name='tenant_foundation_customercomment_created_by_related', to='shared_foundation.O55User'),
            preserve_default=False,
        ),
    ]

# Generated by Django 2.0 on 2018-02-04 04:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tenant_foundation', '0007_auto_20180204_0356'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customercomment',
            name='created_by',
        ),
    ]

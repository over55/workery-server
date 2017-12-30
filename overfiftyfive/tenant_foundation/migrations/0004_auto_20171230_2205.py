# Generated by Django 2.0 on 2017-12-30 22:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tenant_foundation', '0003_auto_20171230_2159'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='is_senior',
            field=models.BooleanField(default=False, help_text='Indicates whether customer is considered a senior or not.', verbose_name='Is Senior'),
        ),
        migrations.AddField(
            model_name='customer',
            name='is_support',
            field=models.BooleanField(default=False, help_text='Indicates whether customer needs support or not.', verbose_name='Is Support'),
        ),
        migrations.AddField(
            model_name='customer',
            name='job_info_read',
            field=models.CharField(blank=True, help_text='-', max_length=31, null=True, verbose_name='Job Info Read'),
        ),
        migrations.AddField(
            model_name='customer',
            name='learn_about',
            field=models.CharField(blank=True, help_text='Describes how this customer heard about Over55.', max_length=63, null=True, verbose_name='Learn About'),
        ),
    ]

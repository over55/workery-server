# Generated by Django 2.0.13 on 2019-10-10 15:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tenant_foundation', '0062_workorderdeposit'),
    ]

    operations = [
        migrations.AddField(
            model_name='workorderdeposit',
            name='created_from',
            field=models.GenericIPAddressField(blank=True, help_text='The IP address of the creator.', null=True, verbose_name='Created from'),
        ),
        migrations.AddField(
            model_name='workorderdeposit',
            name='created_from_is_public',
            field=models.BooleanField(default=False, help_text='Is creator a public IP and is routable.', verbose_name='Is the IP '),
        ),
        migrations.AddField(
            model_name='workorderdeposit',
            name='last_modified_from',
            field=models.GenericIPAddressField(blank=True, help_text='The IP address of the modifier.', null=True, verbose_name='Last modified from'),
        ),
        migrations.AddField(
            model_name='workorderdeposit',
            name='last_modified_from_is_public',
            field=models.BooleanField(default=False, help_text='Is modifier a public IP and is routable.', verbose_name='Is the IP '),
        ),
    ]

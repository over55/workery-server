# Generated by Django 2.0.7 on 2018-08-24 00:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tenant_foundation', '0018_workorder_was_there_financials_inputted'),
    ]

    operations = [
        migrations.AddField(
            model_name='associate',
            name='wsib_number',
            field=models.PositiveIntegerField(blank=True, help_text='The WSIB number associated with the associate.', null=True, verbose_name='WSIB Number'),
        ),
    ]
# Generated by Django 2.0.4 on 2018-05-21 00:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tenant_foundation', '0005_auto_20180520_2311'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='invoice_sub_total_amount',
        ),
        migrations.RemoveField(
            model_name='order',
            name='invoice_sub_total_amount_currency',
        ),
    ]
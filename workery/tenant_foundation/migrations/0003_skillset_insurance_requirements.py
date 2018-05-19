# Generated by Django 2.0.4 on 2018-05-19 21:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tenant_foundation', '0002_auto_20180519_2143'),
    ]

    operations = [
        migrations.AddField(
            model_name='skillset',
            name='insurance_requirements',
            field=models.ManyToManyField(blank=True, help_text='The insurance requirements this associate meets.', related_name='tenant_foundation_skillset_insurance_requirements_related', to='tenant_foundation.InsuranceRequirement'),
        ),
    ]

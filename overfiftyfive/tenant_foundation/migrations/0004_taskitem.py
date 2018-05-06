# Generated by Django 2.0.4 on 2018-05-05 20:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import tenant_foundation.models.taskitem


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('tenant_foundation', '0003_order_follow_up_days_number'),
    ]

    operations = [
        migrations.CreateModel(
            name='TaskItem',
            fields=[
                ('id', models.BigAutoField(db_index=True, default=tenant_foundation.models.taskitem.increment_task_item_id_number, editable=False, primary_key=True, serialize=False)),
                ('type_of', models.PositiveSmallIntegerField(choices=[(1, 'Residential Customer'), (2, 'Commercial Customer'), (3, 'Unknown Customer')], help_text='The type of task item this is.', verbose_name='Type of')),
                ('text', models.CharField(db_index=True, help_text='The text content of this task_item.', max_length=31, unique=True, verbose_name='Text')),
                ('description', models.TextField(blank=True, default='', help_text='A short description of this task_item.', null=True, verbose_name='Description')),
                ('due_date', models.DateField(blank=True, db_index=True, default=tenant_foundation.models.taskitem.get_todays_date, help_text='The date that this task must be finished by.', verbose_name='Due Date')),
                ('is_closed', models.BooleanField(db_index=True, default=False, help_text='Was this task completed or closed?', verbose_name='Is Closed')),
                ('created', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('last_modified', models.DateTimeField(auto_now=True)),
                ('created_by', models.ForeignKey(blank=True, help_text='The user whom created this order.', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='tenant_foundation_taskitem_created_by_related', to=settings.AUTH_USER_MODEL)),
                ('job', models.ForeignKey(help_text='The job order that this task is referencing.', on_delete=django.db.models.deletion.CASCADE, related_name='tenant_foundation_taskitem_job_related', to='tenant_foundation.Order')),
                ('last_modified_by', models.ForeignKey(blank=True, help_text='The user whom last modified this order.', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='tenant_foundation_taskitem_last_modified_by_related', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'TaskItem',
                'verbose_name_plural': 'TaskItems',
                'db_table': 'o55_task_items',
                'ordering': ['-due_date'],
                'permissions': (('can_get_task_items', 'Can get task_items'), ('can_get_task_item', 'Can get task_item'), ('can_post_task_item', 'Can create task_item'), ('can_put_task_item', 'Can update task_item'), ('can_delete_task_item', 'Can delete task_item')),
                'default_permissions': (),
            },
        ),
    ]
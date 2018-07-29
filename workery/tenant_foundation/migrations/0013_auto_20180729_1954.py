# Generated by Django 2.0.7 on 2018-07-29 19:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import tenant_foundation.models.ongoing_work_order
import tenant_foundation.models.ongoing_work_order_comment


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('tenant_foundation', '0012_auto_20180729_1626'),
    ]

    operations = [
        migrations.CreateModel(
            name='OngoingWorkOrderComment',
            fields=[
                ('id', models.BigAutoField(db_index=True, default=tenant_foundation.models.ongoing_work_order_comment.increment_order_comment_id_number, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True)),
            ],
            options={
                'verbose_name': 'Ongoing Work Order Comment',
                'verbose_name_plural': 'Ongoing Work Order Comments',
                'db_table': 'workery_ongoing_work_order_comments',
                'ordering': ['-created_at'],
                'permissions': (('can_get_order_comments', 'Can get order comments'), ('can_get_order_comment', 'Can get order comment'), ('can_post_order_comment', 'Can create order comment'), ('can_put_order_comment', 'Can update order comment'), ('can_delete_order_comment', 'Can delete order comment')),
                'default_permissions': (),
            },
        ),
        migrations.RemoveField(
            model_name='ongoingworkorder',
            name='open_order',
        ),
        migrations.AddField(
            model_name='ongoingworkorder',
            name='assignment_date',
            field=models.DateField(blank=True, help_text='The date that an associate was assigned to the customer.', null=True, verbose_name='Assignment Date'),
        ),
        migrations.AddField(
            model_name='ongoingworkorder',
            name='completion_date',
            field=models.DateField(blank=True, help_text='The date that this ongoing order was completed.', null=True, verbose_name='Completion Date'),
        ),
        migrations.AddField(
            model_name='ongoingworkorder',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, db_index=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='ongoingworkorder',
            name='created_by',
            field=models.ForeignKey(blank=True, help_text='The user whom created this ongoing order.', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='tenant_foundation_ongoingworkorder_created_by_related', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='ongoingworkorder',
            name='created_from',
            field=models.GenericIPAddressField(blank=True, help_text='The IP address of the creator.', null=True, verbose_name='Created from'),
        ),
        migrations.AddField(
            model_name='ongoingworkorder',
            name='created_from_is_public',
            field=models.BooleanField(default=False, help_text='Is creator a public IP and is routable.', verbose_name='Is the IP '),
        ),
        migrations.AddField(
            model_name='ongoingworkorder',
            name='description',
            field=models.TextField(blank=True, default='', help_text='A description of this ongoing order.', null=True, verbose_name='Description'),
        ),
        migrations.AddField(
            model_name='ongoingworkorder',
            name='is_home_support_service',
            field=models.BooleanField(default=False, help_text='Track whether this order is a home support service request.', verbose_name='Is Home Support Service'),
        ),
        migrations.AddField(
            model_name='ongoingworkorder',
            name='last_modified_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='ongoingworkorder',
            name='last_modified_by',
            field=models.ForeignKey(blank=True, help_text='The user whom last modified this ongoing order.', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='tenant_foundation_ongoingworkorder_last_modified_by_related', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='ongoingworkorder',
            name='last_modified_from',
            field=models.GenericIPAddressField(blank=True, help_text='The IP address of the modifier.', null=True, verbose_name='Last modified from'),
        ),
        migrations.AddField(
            model_name='ongoingworkorder',
            name='last_modified_from_is_public',
            field=models.BooleanField(default=False, help_text='Is modifier a public IP and is routable.', verbose_name='Is the IP '),
        ),
        migrations.AddField(
            model_name='ongoingworkorder',
            name='skill_sets',
            field=models.ManyToManyField(blank=True, help_text='The skill sets that belong to this order.', related_name='tenant_foundation_ongoingworkorder_skill_sets_related', to='tenant_foundation.SkillSet'),
        ),
        migrations.AddField(
            model_name='ongoingworkorder',
            name='start_date',
            field=models.DateField(blank=True, default=tenant_foundation.models.ongoing_work_order.get_todays_date, help_text='The date that this ongoing order will begin.', verbose_name='Start Date'),
        ),
        migrations.AddField(
            model_name='ongoingworkorder',
            name='tags',
            field=models.ManyToManyField(blank=True, help_text='The category tags that this order belongs to.', related_name='tenant_foundation_ongoingworkorder_tags_related', to='tenant_foundation.Tag'),
        ),
        migrations.AddField(
            model_name='ongoingworkorder',
            name='type_of',
            field=models.PositiveSmallIntegerField(blank=True, choices=[(1, 'Residential Job Type'), (2, 'Commercial Job Type'), (3, 'Unassigned Job Type')], default=3, help_text='The type of job this is.', verbose_name='Type Of'),
        ),
        migrations.AddField(
            model_name='taskitem',
            name='ongoing_job',
            field=models.ForeignKey(blank=True, help_text='The (ongoing) job order that this task is referencing.', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='tenant_foundation_taskitem_ongoing_job_related', to='tenant_foundation.OngoingWorkOrder'),
        ),
        migrations.AlterField(
            model_name='taskitem',
            name='job',
            field=models.ForeignKey(blank=True, help_text='The job order that this task is referencing.', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='tenant_foundation_taskitem_job_related', to='tenant_foundation.WorkOrder'),
        ),
        migrations.AddField(
            model_name='ongoingworkordercomment',
            name='about',
            field=models.ForeignKey(help_text='The order whom this comment is about.', on_delete=django.db.models.deletion.CASCADE, related_name='tenant_foundation_ongoingworkordercomment_about_related', to='tenant_foundation.OngoingWorkOrder'),
        ),
        migrations.AddField(
            model_name='ongoingworkordercomment',
            name='comment',
            field=models.ForeignKey(help_text='The comment this item belongs to.', on_delete=django.db.models.deletion.CASCADE, related_name='tenant_foundation_ongoingworkordercomment_comment_related', to='tenant_foundation.Comment'),
        ),
        migrations.AddField(
            model_name='ongoingworkorder',
            name='comments',
            field=models.ManyToManyField(blank=True, help_text='The comments belonging to this ongoing order.', related_name='tenant_foundation_ongoingworkorder_ongoing_order_comments_related', through='tenant_foundation.OngoingWorkOrderComment', to='tenant_foundation.Comment'),
        ),
    ]

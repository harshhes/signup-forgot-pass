from django.db import models, migrations
from django.contrib.auth.models import Group
import json

def create_internal_groups(apps, schema_editor):
    admin_group, created = Group.objects.get_or_create(name='Admin')
    teacher_group, created = Group.objects.get_or_create(name='Teacher')
    student_group, created = Group.objects.get_or_create(name='Student')

    admin_group.permissions.set(['base.add_user', 'base.view_user'])
    teacher_group.permissions.set(['base.add_user', 'base.view_user'])
    student_group.permissions.set(['base.view_user'])

    return None

class Migration(migrations.Migration):

    dependencies = [
        ('base', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_internal_groups),
    ]
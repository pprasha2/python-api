# Generated by Django 3.0.7 on 2020-06-08 16:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='IsActive',
            new_name='is_active',
        ),
        migrations.RenameField(
            model_name='user',
            old_name='IsStaff',
            new_name='is_staff',
        ),
    ]
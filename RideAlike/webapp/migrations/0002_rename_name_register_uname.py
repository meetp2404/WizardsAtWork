# Generated by Django 4.1.3 on 2022-11-16 04:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='register',
            old_name='name',
            new_name='uname',
        ),
    ]

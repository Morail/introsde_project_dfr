# Generated by Django 3.0.10 on 2020-09-28 20:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ehr_s_api', '0015_auto_20200928_1913'),
    ]

    operations = [
        migrations.RenameField(
            model_name='prescription',
            old_name='start_date',
            new_name='date',
        ),
    ]
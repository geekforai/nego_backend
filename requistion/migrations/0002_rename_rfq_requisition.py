# Generated by Django 5.1.2 on 2024-10-15 09:47

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('requistion', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RenameModel(
            old_name='RFQ',
            new_name='Requisition',
        ),
    ]

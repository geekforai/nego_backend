# Generated by Django 5.1.2 on 2024-10-15 11:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0002_alter_chat_created_by'),
    ]

    operations = [
        migrations.RenameField(
            model_name='chat',
            old_name='requisition',
            new_name='requisition_id',
        ),
    ]

# Generated by Django 5.1.2 on 2024-10-16 05:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0005_remove_chat_id_alter_chat_chat_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='chat',
            name='feedback',
            field=models.TextField(default=None),
        ),
    ]

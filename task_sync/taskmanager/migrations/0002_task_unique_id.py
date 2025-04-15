# Generated by Django 5.1.7 on 2025-04-14 09:51

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('taskmanager', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='unique_id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, unique=True),
        ),
    ]

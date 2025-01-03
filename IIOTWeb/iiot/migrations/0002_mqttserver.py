# Generated by Django 5.1.1 on 2024-11-06 07:34

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('iiot', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='MqttServer',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('device_name', models.CharField(max_length=24)),
                ('ip_address', models.GenericIPAddressField()),
                ('port', models.IntegerField()),
                ('mqtt_user_name', models.CharField(max_length=24)),
                ('mqtt_password', models.CharField(max_length=24)),
            ],
        ),
    ]

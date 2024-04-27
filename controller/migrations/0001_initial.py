# Generated by Django 4.2 on 2024-04-21 07:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('api', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='verifyTable_Model',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('srcIP', models.CharField(max_length=17)),
                ('inInterfaceId', models.CharField(max_length=15)),
                ('deviceId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.devicemodel')),
            ],
        ),
        migrations.CreateModel(
            name='RIB_Model',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('srcIP', models.CharField(max_length=17)),
                ('dstIP', models.CharField(max_length=17)),
                ('nextHop', models.CharField(max_length=15)),
                ('inInterfaceId', models.IntegerField()),
                ('outInterfaceId', models.IntegerField()),
                ('deviceId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.devicemodel')),
            ],
        ),
        migrations.CreateModel(
            name='FIB_Model',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('dstIP', models.CharField(max_length=17)),
                ('outInterfaceId', models.CharField(max_length=15)),
                ('deviceId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.devicemodel')),
            ],
        ),
    ]

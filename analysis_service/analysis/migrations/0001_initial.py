# Generated by Django 3.2 on 2022-04-06 18:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Airport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, unique=True)),
                ('city', models.CharField(max_length=128)),
            ],
        ),
        migrations.CreateModel(
            name='Carrier',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, unique=True)),
                ('rating', models.PositiveIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='PlaneType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, unique=True)),
                ('capacity', models.PositiveIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Flight',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField()),
                ('sit_class', models.CharField(max_length=16)),
                ('price', models.PositiveIntegerField()),
                ('carrier', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='flights', to='planes.carrier')),
                ('dest_airport', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='in_flights', to='planes.airport')),
                ('origin_airport', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='out_flights', to='planes.airport')),
                ('plane_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='flights', to='planes.planetype')),
            ],
        ),
    ]
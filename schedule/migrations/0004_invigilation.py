# Generated by Django 4.2.7 on 2024-11-18 11:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_alter_room_block'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('schedule', '0003_rename_sectionid_schedule_section'),
    ]

    operations = [
        migrations.CreateModel(
            name='Invigilation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('examDate', models.DateField()),
                ('examTime', models.TimeField()),
                ('invigilator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.room')),
            ],
            options={
                'unique_together': {('room', 'examDate', 'examTime', 'invigilator')},
            },
        ),
    ]

# Generated by Django 4.2.7 on 2024-10-17 09:37

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_course_section'),
    ]

    operations = [
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=15, validators=[django.core.validators.MinLengthValidator(2)])),
                ('room_type', models.PositiveIntegerField(choices=[(10, 'Classroom'), (20, 'Computer Lab'), (30, 'Physics Lab'), (40, 'Chemistry Lab'), (50, 'CAD Workshop'), (60, 'Lecture Hall')])),
                ('campus', models.CharField(choices=[('SA', 'Al Saada Campus'), ('AK', 'Al Akhdar Campus')], max_length=10, validators=[django.core.validators.MinLengthValidator(2)])),
                ('capacity', models.PositiveBigIntegerField()),
                ('block', models.CharField(max_length=15, validators=[django.core.validators.MinLengthValidator(2)])),
            ],
        ),
        migrations.AlterField(
            model_name='department',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True, unique=True),
        ),
        migrations.AddConstraint(
            model_name='room',
            constraint=models.UniqueConstraint(fields=('label', 'campus'), name='unique_room_label_campus'),
        ),
    ]

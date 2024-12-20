# Generated by Django 4.2.7 on 2024-11-07 10:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_room_alter_department_email_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='room',
            name='room_type',
            field=models.PositiveIntegerField(choices=[(10, 'Classroom'), (20, 'Computer Lab'), (30, 'Physics Lab'), (40, 'Chemistry Lab'), (50, 'CAD Workshop'), (60, 'Lecture Hall')], default=10),
        ),
        migrations.CreateModel(
            name='Registration',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('registration_date', models.DateField(auto_now_add=True)),
                ('status', models.CharField(choices=[('A', 'Active'), ('C', 'Completed'), ('W', 'Withdrawal')], default='active', max_length=50)),
                ('section', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.section')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.student')),
            ],
            options={
                'unique_together': {('student', 'section')},
            },
        ),
    ]

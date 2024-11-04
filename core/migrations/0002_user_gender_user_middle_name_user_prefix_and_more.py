# Generated by Django 4.2.7 on 2024-10-08 10:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='gender',
            field=models.CharField(blank=True, choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other')], max_length=1, null=True, verbose_name='Gender'),
        ),
        migrations.AddField(
            model_name='user',
            name='middle_name',
            field=models.CharField(blank=True, max_length=150, null=True, verbose_name='Middle Name'),
        ),
        migrations.AddField(
            model_name='user',
            name='prefix',
            field=models.CharField(blank=True, choices=[('Mr', 'Mr.'), ('Ms', 'Ms.'), ('Mrs', 'Mrs.'), ('Dr', 'Dr.'), ('Prof', 'Prof.')], max_length=10, null=True, verbose_name='Prefix'),
        ),
        migrations.AlterField(
            model_name='user',
            name='first_name',
            field=models.CharField(max_length=150, verbose_name='First Name'),
        ),
        migrations.AlterField(
            model_name='user',
            name='last_name',
            field=models.CharField(max_length=150, verbose_name='Last Name'),
        ),
    ]

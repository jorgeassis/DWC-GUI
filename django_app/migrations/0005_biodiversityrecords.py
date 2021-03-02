# Generated by Django 3.1.3 on 2020-11-10 14:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('django_app', '0004_djangousers_usertype'),
    ]

    operations = [
        migrations.CreateModel(
            name='biodiversityRecords',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('loginName', models.CharField(default='NA', max_length=255)),
                ('firstName', models.CharField(default='NA', max_length=255)),
                ('lastName', models.CharField(default='NA', max_length=255)),
                ('email', models.CharField(default='NA', max_length=255)),
                ('userType', models.CharField(default='NA', max_length=255)),
            ],
            options={
                'verbose_name_plural': 'records',
            },
        ),
    ]
# Generated by Django 3.1.3 on 2020-11-10 18:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('django_app', '0012_auto_20201110_1848'),
    ]

    operations = [
        migrations.AlterField(
            model_name='biodiversityrecords',
            name='SampleN',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='biodiversityrecords',
            name='bibliographicCitation',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='biodiversityrecords',
            name='coordinateUncertaintyInMeters',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='biodiversityrecords',
            name='day',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='biodiversityrecords',
            name='decimalLatitude',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='biodiversityrecords',
            name='decimalLongitude',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='biodiversityrecords',
            name='fieldNotes',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='biodiversityrecords',
            name='georeferenceRemarks',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='biodiversityrecords',
            name='identificationRemarks',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='biodiversityrecords',
            name='individualCount',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='biodiversityrecords',
            name='license',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='biodiversityrecords',
            name='maximumDepthInMeters',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='biodiversityrecords',
            name='measurementRemarks',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='biodiversityrecords',
            name='measurementValue',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='biodiversityrecords',
            name='minimumDepthInMeters',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='biodiversityrecords',
            name='month',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='biodiversityrecords',
            name='namePublishedInYear',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='biodiversityrecords',
            name='organismQuantity',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='biodiversityrecords',
            name='recordNumber',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='biodiversityrecords',
            name='sampleSizeValue',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='biodiversityrecords',
            name='taxonRemarks',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='biodiversityrecords',
            name='verbatimDepth',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='biodiversityrecords',
            name='year',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
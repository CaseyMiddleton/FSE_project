# Generated by Django 4.0.3 on 2022-04-26 21:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scrappy_webpage', '0008_searches_cleaned_data_searches_raw_data'),
    ]

    operations = [
        migrations.AlterField(
            model_name='searches',
            name='cleaned_data',
            field=models.CharField(default='X', max_length=10000),
        ),
        migrations.AlterField(
            model_name='searches',
            name='raw_data',
            field=models.CharField(default='X', max_length=100000),
        ),
    ]

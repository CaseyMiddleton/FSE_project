# Generated by Django 4.0.3 on 2022-04-15 19:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scrappy_webpage', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='searches',
            name='first_query',
            field=models.CharField(max_length=245),
        ),
    ]

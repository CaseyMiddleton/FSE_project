# Generated by Django 4.0.3 on 2022-04-15 20:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scrappy_webpage', '0003_searches_connector_searches_second_query'),
    ]

    operations = [
        migrations.AlterField(
            model_name='searches',
            name='connector',
            field=models.CharField(choices=[('and', 'and'), ('or', 'or')], default='and', max_length=100),
        ),
        migrations.AlterField(
            model_name='searches',
            name='first_query',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='searches',
            name='second_query',
            field=models.CharField(max_length=200),
        ),
    ]

# Generated by Django 5.1.3 on 2024-11-22 01:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('emo_calendar', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mymoodhistory',
            name='date',
            field=models.DateField(),
        ),
    ]

# Generated by Django 2.0.6 on 2018-06-12 23:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20180612_2344'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='points_scored',
            field=models.IntegerField(default=0),
        ),
    ]

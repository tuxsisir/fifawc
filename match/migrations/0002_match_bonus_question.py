# Generated by Django 2.0.6 on 2018-06-14 17:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('match', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='match',
            name='bonus_question',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
    ]

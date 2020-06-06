# Generated by Django 2.0.6 on 2018-06-12 21:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('match', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Prediction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('home_goal', models.PositiveSmallIntegerField(default=0)),
                ('away_goal', models.PositiveSmallIntegerField(default=0)),
                ('red_card', models.BooleanField(default=False)),
                ('yellow_card', models.BooleanField(default=True)),
                ('match', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='predictions', to='match.Match')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='my_predictions', to=settings.AUTH_USER_MODEL)),
                ('winning_team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='win_predicted', to='match.Country')),
            ],
        ),
    ]

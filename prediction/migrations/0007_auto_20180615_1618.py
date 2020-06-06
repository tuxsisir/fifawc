# Generated by Django 2.0.6 on 2018-06-15 10:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('prediction', '0006_pointscored_last_increased_by'),
    ]

    operations = [
        migrations.AlterField(
            model_name='matchoutcome',
            name='winning_team',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='match_won', to='match.Country'),
        ),
        migrations.AlterField(
            model_name='prediction',
            name='winning_team',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='win_predicted', to='match.Country'),
        ),
    ]
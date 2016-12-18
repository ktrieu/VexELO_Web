# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2016-12-18 01:47
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Match',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('redScore', models.IntegerField()),
                ('blueScore', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=10)),
                ('elo', models.FloatField()),
            ],
        ),
        migrations.AddField(
            model_name='match',
            name='blueTeam1',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='blueTeam1_set', to='VexELO_rankings.Team'),
        ),
        migrations.AddField(
            model_name='match',
            name='blueTeam2',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='blueTeam2_set', to='VexELO_rankings.Team'),
        ),
        migrations.AddField(
            model_name='match',
            name='redTeam1',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='redTeam1_set', to='VexELO_rankings.Team'),
        ),
        migrations.AddField(
            model_name='match',
            name='redTeam2',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='redTeam2_set', to='VexELO_rankings.Team'),
        ),
    ]
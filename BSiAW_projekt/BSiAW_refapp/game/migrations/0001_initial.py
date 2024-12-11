# Generated by Django 5.1.4 on 2024-12-11 01:17

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Klub',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
                ('liga', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Match',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('wynik', models.CharField(default='0:0', max_length=8)),
                ('status', models.CharField(choices=[('przed', 'Przed'), ('zlozone', 'Złożone'), ('zaakceptowane', 'Zaakceptowane')], default='przed', max_length=20)),
                ('data', models.DateField(null=True)),
                ('godzina', models.CharField(max_length=10, null=True)),
                ('ulica', models.CharField(max_length=100, null=True)),
                ('miejscowosc', models.CharField(max_length=100, null=True)),
                ('rozgrywki', models.CharField(max_length=100, null=True)),
                ('runda', models.CharField(choices=[('jesien', 'Jesienna'), ('wiosna', 'Wiosenna')], max_length=20, null=True)),
                ('kolejka', models.PositiveIntegerField(null=True)),
                ('Gosc', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='gosc_mecze', to='game.klub')),
                ('Gosp', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='gospodarz_mecze', to='game.klub')),
                ('Kolegium', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='kolegium_mecz', to=settings.AUTH_USER_MODEL)),
                ('SedziaA1', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='szedziaa1_meczu', to=settings.AUTH_USER_MODEL)),
                ('SedziaA2', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='szedziaa2_meczu', to=settings.AUTH_USER_MODEL)),
                ('SedziaG', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='szedziag_meczu', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Events',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('typ', models.CharField(choices=[('zolta_kartka', 'Zolta_kartka'), ('czerwona_kartka', 'Czerwona_kartka'), ('gol', 'Gol')], max_length=50)),
                ('minuta', models.IntegerField()),
                ('kto', models.CharField(choices=[('gosp', 'Gospodarz'), ('gosc', 'Gosc')], max_length=50)),
                ('nr_zawodnika', models.IntegerField()),
                ('mecz', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='wydarzenie_meczowe', to='game.match')),
            ],
        ),
        migrations.CreateModel(
            name='Zawodnik',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('imie', models.CharField(max_length=50)),
                ('nazwisko', models.CharField(max_length=50)),
                ('nr', models.IntegerField()),
                ('klub', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='zawodnicy', to='game.klub')),
            ],
        ),
    ]

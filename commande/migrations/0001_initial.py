# Generated by Django 5.0.7 on 2024-07-25 20:51

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
            name='Plat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('prix', models.DecimalField(decimal_places=2, max_digits=6)),
                ('allergenes', models.TextField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Commande',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('montant_total', models.DecimalField(decimal_places=2, max_digits=8)),
                ('date_commande', models.DateTimeField(auto_now_add=True)),
                ('confirme', models.BooleanField(default=False)),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='CommandePlat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantite', models.PositiveIntegerField()),
                ('commande', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='commande.commande')),
                ('plat', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='commande.plat')),
            ],
        ),
        migrations.AddField(
            model_name='commande',
            name='plats',
            field=models.ManyToManyField(through='commande.CommandePlat', to='commande.plat'),
        ),
    ]

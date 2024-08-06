# Generated by Django 5.0.7 on 2024-08-01 10:22

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestion', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='StockMovement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_mouvement', models.DateTimeField(default=django.utils.timezone.now)),
                ('quantite', models.FloatField()),
                ('mouvement_type', models.CharField(choices=[('entrée', 'Entrée'), ('sortie', 'Sortie')], max_length=10)),
                ('commentaire', models.TextField(blank=True, null=True)),
                ('ingredient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gestion.ingredient')),
            ],
        ),
    ]

# Generated by Django 5.0.7 on 2024-07-26 15:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('commande', '0006_rename_category_categorie'),
    ]

    operations = [
        migrations.AddField(
            model_name='commandeplat',
            name='commentaire',
            field=models.TextField(blank=True, null=True),
        ),
    ]

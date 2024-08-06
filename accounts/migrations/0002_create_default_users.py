# accounts/migrations/0002_create_default_users.py

from django.db import migrations
from django.contrib.auth.hashers import make_password

def create_users(apps, schema_editor):
    CustomUser = apps.get_model('accounts', 'User')
    
    users = [
        {'username': 'caissier', 'email': 'caissier5@gmail.com', 'password': 'caissiercicare', 'role': 'caissier'},
        {'username': 'comptable', 'email': 'comptable123@example.com', 'password': 'comptable123', 'role': 'comptable'},
        {'username': 'responsable', 'email': 'responsable123@example.com', 'password': 'respond156', 'role': 'responsable'},
    ]

    for user_data in users:
        user_data['password'] = make_password(user_data['password'])
        CustomUser.objects.create(**user_data)

class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_users),
    ]

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from django.contrib.auth.models import User

username = os.environ.get('ADMIN_USER', 'admin')
password = os.environ.get('ADMIN_PASS', 'admin123')
email = os.environ.get('ADMIN_EMAIL', 'admin@ct.gov.br')

if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username=username, password=password, email=email)
    print(f'Superusuário "{username}" criado com sucesso!')
else:
    print(f'Usuário "{username}" já existe.')

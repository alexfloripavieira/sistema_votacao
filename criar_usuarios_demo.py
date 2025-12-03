#!/usr/bin/env python3
"""
Script para criar usuários de demonstração
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from django.contrib.auth.models import User

def create_demo_users():
    # Criar admin
    if not User.objects.filter(username='demo_admin').exists():
        admin = User.objects.create_superuser(
            username='demo_admin',
            email='admin@avai.com',
            password='demo123',
            first_name='Admin',
            last_name='Avaí'
        )
        print(f'✅ Admin criado: {admin.username}')
    else:
        print('ℹ️  Admin já existe: demo_admin')

    # Criar usuário comum
    if not User.objects.filter(username='demo_user').exists():
        user = User.objects.create_user(
            username='demo_user',
            email='usuario@avai.com',
            password='demo123',
            first_name='João',
            last_name='Silva'
        )
        print(f'✅ Usuário comum criado: {user.username}')
    else:
        print('ℹ️  Usuário comum já existe: demo_user')

    # Criar mais alguns usuários para preencher a lista
    for i in range(1, 4):
        username = f'conselheiro{i}'
        if not User.objects.filter(username=username).exists():
            user = User.objects.create_user(
                username=username,
                email=f'conselheiro{i}@avai.com',
                password='demo123',
                first_name=f'Conselheiro',
                last_name=f'Número {i}'
            )
            print(f'✅ Usuário criado: {user.username}')

if __name__ == '__main__':
    print('🔧 Criando usuários de demonstração...')
    print()
    create_demo_users()
    print()
    print('✅ Pronto!')

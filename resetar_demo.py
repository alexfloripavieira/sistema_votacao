#!/usr/bin/env python3
"""
Script para resetar o sistema para demonstração
"""

import os

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
django.setup()

import datetime

from django.contrib.auth.models import User
from django.utils import timezone

from business.models import Meeting, Presence, Vote, Voting


def reset_demo():
    print("🔄 Resetando sistema para demonstração...\n")

    # 1. Fechar todas as reuniões ativas
    active_meetings = Meeting.objects.filter(is_active=True)
    for meeting in active_meetings:
        meeting.is_active = False
        meeting.closed_at = timezone.now()
        meeting.save()
    print(f"✅ {active_meetings.count()} reunião(ões) fechada(s)")

    # 2. Deletar todas as votações
    voting_count = Voting.objects.all().count()
    Voting.objects.all().delete()
    print(f"✅ {voting_count} votação(ões) removida(s)")

    # 3. Limpar todos os votos
    Vote.objects.all().delete()
    print("✅ Votos removidos")

    # 4. Garantir que usuários de demo existem
    if not User.objects.filter(username="demo_admin").exists():
        User.objects.create_superuser(
            username="demo_admin",
            email="admin@avai.com",
            password="demo123",
            first_name="Admin",
            last_name="Avaí",
        )
        print("✅ Admin criado")
    else:
        print("ℹ️  Admin já existe")

    if not User.objects.filter(username="demo_user").exists():
        User.objects.create_user(
            username="demo_user",
            email="usuario@avai.com",
            password="demo123",
            first_name="João",
            last_name="Silva",
        )
        print("✅ Usuário comum criado")
    else:
        print("ℹ️  Usuário comum já existe")

    # 5. Criar nova reunião ativa
    admin = User.objects.get(username="demo_admin")
    from django.utils import timezone

    meeting = Meeting.objects.create(
        meeting_date=datetime.date.today(),
        is_active=True,
        created_by=admin,
        created_at=timezone.now(),
    )
    print(f"✅ Nova reunião criada: {meeting.meeting_date}")

    # 6. Criar registros de presença para todos os usuários
    users = User.objects.all()
    for user in users:
        Presence.objects.create(user=user, meeting=meeting, present=False)
    print(f"✅ {users.count()} registros de presença criados")

    # 7. Marcar presença do demo_user
    demo_user = User.objects.get(username="demo_user")
    presence = Presence.objects.get(user=demo_user, meeting=meeting)
    presence.present = True
    presence.save()
    print("✅ Presença do demo_user marcada!")

    print("\n✅ Sistema resetado e pronto para demonstração!")


if __name__ == "__main__":
    reset_demo()

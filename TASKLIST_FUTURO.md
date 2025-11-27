# Lista de Tarefas - Sistema de Votação Avaí FC
## Desenvolvimento Futuro (Sprints 7-10)

Baseado no PRD_FUTURO.md - Implementação granular das próximas funcionalidades.

---

## 🎯 SPRINT 7: INFRAESTRUTURA E PRODUÇÃO
**Duração Estimada**: 3-4 dias
**Prioridade**: 🔴 Alta

### 7.1 Deploy em Servidor de Produção
**Status**: ⏳ Pendente
**Tempo Estimado**: 2-3 dias

#### 7.1.1 Configuração do Servidor Linux
- [ ] **Escolher provedor de hospedagem** (DigitalOcean, Linode, AWS Lightsail)
- [ ] **Criar instância Ubuntu 22.04 LTS** (2GB RAM, 1 vCPU mínimo)
- [ ] **Configurar usuário não-root** com sudo
- [ ] **Atualizar sistema** (`sudo apt update && sudo apt upgrade`)
- [ ] **Instalar pacotes essenciais** (curl, wget, git, htop, ufw)
- [ ] **Configurar firewall UFW** (SSH, HTTP, HTTPS)
- [ ] **Configurar timezone** (`sudo timedatectl set-timezone America/Sao_Paulo`)

#### 7.1.2 Instalação do PostgreSQL
- [ ] **Instalar PostgreSQL** (`sudo apt install postgresql postgresql-contrib`)
- [ ] **Iniciar serviço** (`sudo systemctl start postgresql`)
- [ ] **Criar banco de dados** (`createdb avai_voting`)
- [ ] **Criar usuário do banco** (`createuser avai_user`)
- [ ] **Configurar permissões** (`GRANT ALL PRIVILEGES ON DATABASE avai_voting TO avai_user`)
- [ ] **Configurar senha segura** para o usuário do banco

#### 7.1.3 Instalação do Python e Dependências
- [ ] **Instalar Python 3.11+** (`sudo apt install python3.11 python3.11-venv`)
- [ ] **Criar ambiente virtual** (`python3 -m venv /opt/avai-voting/venv`)
- [ ] **Clonar repositório** (`git clone https://github.com/user/avai-voting.git`)
- [ ] **Instalar dependências** (`pip install -r requirements.txt`)
- [ ] **Instalar dependências de produção** (gunicorn, psycopg2-binary)

#### 7.1.4 Configuração do Gunicorn
- [ ] **Criar arquivo gunicorn.conf.py**
  ```python
  bind = "127.0.0.1:8000"
  workers = 3
  user = "avai"
  group = "avai"
  tmp_upload_dir = None
  ```
- [ ] **Criar serviço systemd** (`/etc/systemd/system/avai-voting.service`)
- [ ] **Configurar auto-start** (`sudo systemctl enable avai-voting`)
- [ ] **Testar inicialização** (`sudo systemctl start avai-voting`)

#### 7.1.5 Configuração do Nginx
- [ ] **Instalar Nginx** (`sudo apt install nginx`)
- [ ] **Criar configuração do site** (`/etc/nginx/sites-available/avai-voting`)
  ```
  server {
      listen 80;
      server_name votacao.avaifc.com.br;

      location = /favicon.ico { access_log off; log_not_found off; }

      location /static/ {
          alias /opt/avai-voting/static/;
      }

      location / {
          include proxy_params;
          proxy_pass http://127.0.0.1:8000;
      }
  }
  ```
- [ ] **Habilitar site** (`sudo ln -s /etc/nginx/sites-available/avai-voting /etc/nginx/sites-enabled`)
- [ ] **Testar configuração** (`sudo nginx -t`)
- [ ] **Reiniciar Nginx** (`sudo systemctl restart nginx`)

#### 7.1.6 Configuração de Domínio
- [ ] **Registrar domínio** (votacao.avaifc.com.br)
- [ ] **Configurar DNS** (apontar A record para IP do servidor)
- [ ] **Atualizar ALLOWED_HOSTS** no settings.py
- [ ] **Testar acesso** via domínio

#### 7.1.7 Logs e Monitoramento Básico
- [ ] **Configurar logrotate** para logs do Django
- [ ] **Instalar htop** para monitoramento básico
- [ ] **Configurar log do Nginx** (`/var/log/nginx/`)
- [ ] **Criar script de monitoramento** (uptime, uso de CPU/memória)

### 7.2 Configuração HTTPS
**Status**: ⏳ Pendente
**Tempo Estimado**: 1 dia

#### 7.2.1 Instalação do Certbot
- [ ] **Instalar snap** (`sudo apt install snapd`)
- [ ] **Instalar certbot** (`sudo snap install core; sudo snap refresh core`)
- [ ] **Instalar plugin Nginx** (`sudo snap install --classic certbot`)
- [ ] **Criar link simbólico** (`sudo ln -s /snap/bin/certbot /usr/bin/certbot`)

#### 7.2.2 Geração do Certificado SSL
- [ ] **Executar certbot** (`sudo certbot --nginx -d votacao.avaifc.com.br`)
- [ ] **Escolher opção 2** (redirect HTTP to HTTPS)
- [ ] **Verificar certificado** (`sudo certbot certificates`)
- [ ] **Testar HTTPS** (https://votacao.avaifc.com.br)

#### 7.2.3 Configuração de Segurança
- [ ] **Adicionar headers de segurança** no Nginx:
  ```
  add_header X-Frame-Options "SAMEORIGIN" always;
  add_header X-Content-Type-Options "nosniff" always;
  add_header X-XSS-Protection "1; mode=block" always;
  add_header Referrer-Policy "strict-origin-when-cross-origin" always;
  ```
- [ ] **Configurar HSTS** (`add_header Strict-Transport-Security "max-age=31536000" always;`)
- [ ] **Configurar CSP** básico
- [ ] **Testar headers** (usar curl ou browser dev tools)

#### 7.2.4 Renovação Automática
- [ ] **Verificar cron job** (`sudo crontab -l`)
- [ ] **Testar renovação** (`sudo certbot renew --dry-run`)
- [ ] **Configurar alerta** para expiração próxima

### 7.3 Backup Automático do Banco
**Status**: ⏳ Pendente
**Tempo Estimado**: 1-2 dias

#### 7.3.1 Configuração do PostgreSQL Backup
- [ ] **Instalar pg_dump** (já incluído com PostgreSQL)
- [ ] **Criar diretório de backup** (`sudo mkdir -p /opt/avai-backups`)
- [ ] **Configurar permissões** (`sudo chown avai:avai /opt/avai-backups`)

#### 7.3.2 Script de Backup
- [ ] **Criar script `/opt/avai-voting/backup.sh`**:
  ```bash
  #!/bin/bash
  DATE=$(date +%Y%m%d_%H%M%S)
  BACKUP_DIR="/opt/avai-backups"
  DB_NAME="avai_voting"
  DB_USER="avai_user"

  # Backup do banco
  pg_dump -U $DB_USER -h localhost $DB_NAME > $BACKUP_DIR/db_$DATE.sql

  # Backup de arquivos estáticos
  tar -czf $BACKUP_DIR/static_$DATE.tar.gz /opt/avai-voting/static/

  # Limpar backups antigos (manter 7 dias)
  find $BACKUP_DIR -name "db_*.sql" -mtime +7 -delete
  find $BACKUP_DIR -name "static_*.tar.gz" -mtime +7 -delete
  ```
- [ ] **Tornar executável** (`chmod +x /opt/avai-voting/backup.sh`)

#### 7.3.3 Agendamento Automático
- [ ] **Criar cron job** (`crontab -e`):
  ```
  # Backup diário às 2:00 AM
  0 2 * * * /opt/avai-voting/backup.sh
  ```
- [ ] **Testar execução manual** (`/opt/avai-voting/backup.sh`)

#### 7.3.4 Backup para Nuvem
- [ ] **Instalar AWS CLI** (`sudo apt install awscli`)
- [ ] **Configurar credenciais AWS** (`aws configure`)
- [ ] **Criar bucket S3** (`avai-voting-backups`)
- [ ] **Modificar script** para upload:
  ```bash
  # Upload para S3 (manter 30 dias)
  aws s3 sync $BACKUP_DIR s3://avai-voting-backups/ --delete --exclude "*" --include "db_*.sql" --include "static_*.tar.gz"
  ```

#### 7.3.5 Teste de Restauração
- [ ] **Criar banco de teste** (`createdb avai_test`)
- [ ] **Restaurar backup** (`psql -U avai_user avai_test < backup.sql`)
- [ ] **Verificar integridade** dos dados
- [ ] **Testar aplicação** com banco restaurado

#### 7.3.6 Notificações de Backup
- [ ] **Adicionar ao script**:
  ```bash
  # Enviar email de sucesso/falha
  if [ $? -eq 0 ]; then
      echo "Backup concluído com sucesso" | mail -s "Backup Avaí OK" admin@avaifc.com.br
  else
      echo "Falha no backup" | mail -s "Backup Avaí FALHA" admin@avaifc.com.br
  fi
  ```
- [ ] **Configurar postfix** para envio de emails

---

## 🎯 SPRINT 8: RELATÓRIOS AVANÇADOS
**Duração Estimada**: 3-4 dias
**Prioridade**: 🟡 Média

### 8.1 Export PDF/Excel - Relatórios de Presença
**Status**: ⏳ Pendente
**Tempo Estimado**: 1.5 dias

#### 8.1.1 Instalação de Dependências
- [ ] **Adicionar ao requirements.txt**:
  ```
  reportlab==4.0.7
  openpyxl==3.1.2
  pandas==2.1.3
  ```
- [ ] **Instalar dependências** (`pip install -r requirements.txt`)

#### 8.1.2 Criação do Utilitário PDF
- [ ] **Criar arquivo** `business/utils.py`
- [ ] **Implementar classe** `PresencePDFExporter`:
  ```python
  from reportlab.lib import colors
  from reportlab.lib.pagesizes import letter, A4
  from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
  from reportlab.lib.styles import getSampleStyleSheet

  class PresencePDFExporter:
      def __init__(self, queryset, start_date=None, end_date=None):
          self.queryset = queryset
          self.start_date = start_date
          self.end_date = end_date

      def generate_pdf(self, filename):
          doc = SimpleDocTemplate(filename, pagesize=A4)
          elements = []

          # Título
          styles = getSampleStyleSheet()
          title = Paragraph("Relatório de Presença - Avaí FC", styles['Heading1'])
          elements.append(title)

          # Dados da tabela
          data = [['Usuário', 'Data', 'Presente']]
          for presence in self.queryset:
              data.append([
                  presence.user.get_full_name() or presence.user.username,
                  presence.meeting.meeting_date.strftime('%d/%m/%Y'),
                  'Sim' if presence.present else 'Não'
              ])

          table = Table(data)
          table.setStyle(TableStyle([
              ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
              ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
              ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
              ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
              ('FONTSIZE', (0, 0), (-1, 0), 14),
              ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
              ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
              ('GRID', (0, 0), (-1, -1), 1, colors.black)
          ]))

          elements.append(table)
          doc.build(elements)
  ```

#### 8.1.3 View de Export PDF
- [ ] **Modificar** `PresenceReportView` para incluir botão de export
- [ ] **Adicionar método** `export_pdf`:
  ```python
  def export_pdf(self, request):
      start_date = request.GET.get('start_date')
      end_date = request.GET.get('end_date')

      queryset = self.get_queryset()
      if start_date:
          queryset = queryset.filter(meeting__meeting_date__gte=start_date)
      if end_date:
          queryset = queryset.filter(meeting__meeting_date__lte=end_date)

      exporter = PresencePDFExporter(queryset, start_date, end_date)
      filename = f"presencas_{start_date}_{end_date}.pdf"

      response = HttpResponse(content_type='application/pdf')
      response['Content-Disposition'] = f'attachment; filename="{filename}"'

      exporter.generate_pdf(response)
      return response
  ```

#### 8.1.4 Template com Botão de Export
- [ ] **Modificar** `presence_report.html`
- [ ] **Adicionar botão** "Exportar PDF" no topo
- [ ] **Adicionar botão** "Exportar Excel" no topo

#### 8.1.5 Implementação Excel Export
- [ ] **Criar classe** `PresenceExcelExporter`:
  ```python
  import pandas as pd
  from openpyxl import Workbook
  from openpyxl.styles import Font, PatternFill

  class PresenceExcelExporter:
      def __init__(self, queryset, start_date=None, end_date=None):
          self.queryset = queryset
          self.start_date = start_date
          self.end_date = end_date

      def generate_excel(self, filename):
          wb = Workbook()
          ws = wb.active
          ws.title = "Relatório de Presença"

          # Cabeçalhos
          headers = ['Usuário', 'Data', 'Presente']
          for col, header in enumerate(headers, 1):
              cell = ws.cell(row=1, column=col, value=header)
              cell.font = Font(bold=True)
              cell.fill = PatternFill(start_color="CCCCCC", end_color="CCCCCC", fill_type="solid")

          # Dados
          for row, presence in enumerate(self.queryset, 2):
              ws.cell(row=row, column=1, value=presence.user.get_full_name() or presence.user.username)
              ws.cell(row=row, column=2, value=presence.meeting.meeting_date.strftime('%d/%m/%Y'))
              ws.cell(row=row, column=3, value='Sim' if presence.present else 'Não')

          wb.save(filename)
  ```

#### 8.1.6 Teste dos Exports
- [ ] **Testar export PDF** com dados de teste
- [ ] **Testar export Excel** com dados de teste
- [ ] **Verificar formatação** dos arquivos gerados
- [ ] **Testar filtros** de data nos exports

### 8.2 Export PDF/Excel - Resultados de Votação
**Status**: ⏳ Pendente
**Tempo Estimado**: 1.5 dias

#### 8.2.1 Utilitário de Export para Votações
- [ ] **Criar classe** `VotingPDFExporter` em `utils.py`
- [ ] **Implementar template** profissional com:
  - Título da votação
  - Período de votação
  - Total de votos
  - Resultados por opção (com percentuais)
  - Lista de votantes (opcional)

#### 8.2.2 View de Export para Votações
- [ ] **Modificar** `VotingReportView` para incluir exports
- [ ] **Adicionar métodos** `export_pdf` e `export_excel`
- [ ] **Implementar lógica** de agregação de dados

#### 8.2.3 Template com Gráficos
- [ ] **Adicionar matplotlib** para geração de gráficos
- [ ] **Implementar** gráfico de barras para resultados
- [ ] **Incluir gráfico** no PDF exportado

#### 8.2.4 Teste Completo
- [ ] **Testar export** de votações simples
- [ ] **Testar export** com múltiplas opções
- [ ] **Verificar gráficos** gerados corretamente
- [ ] **Testar performance** com votações grandes

---

## 🎯 SPRINT 9: COMUNICAÇÃO E NOTIFICAÇÕES
**Duração Estimada**: 2-3 dias
**Prioridade**: 🟡 Média

### 9.1 Configuração do Sistema de Email
**Status**: ⏳ Pendente
**Tempo Estimado**: 1 dia

#### 9.1.1 Instalação e Configuração
- [ ] **Adicionar ao requirements.txt**:
  ```
  django-anymail==10.2
  celery==5.3.4
  redis==5.0.1
  ```
- [ ] **Instalar Redis** (`sudo apt install redis-server`)
- [ ] **Configurar Redis** (`sudo systemctl start redis-server`)

#### 9.1.2 Configuração Django
- [ ] **Atualizar settings.py**:
  ```python
  # Email configuration
  EMAIL_BACKEND = 'anymail.backends.sendgrid.EmailBackend'
  ANYMAIL = {
      'SENDGRID_API_KEY': os.getenv('SENDGRID_API_KEY'),
  }
  DEFAULT_FROM_EMAIL = 'Sistema de Votação <noreply@votacao.avaifc.com.br>'

  # Celery configuration
  CELERY_BROKER_URL = 'redis://localhost:6379/0'
  CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
  ```

#### 9.1.3 Configuração SendGrid
- [ ] **Criar conta** no SendGrid
- [ ] **Verificar domínio** (votacao.avaifc.com.br)
- [ ] **Gerar API Key**
- [ ] **Configurar variável** `SENDGRID_API_KEY`

#### 9.1.4 Teste de Email
- [ ] **Criar comando** `test_email.py`:
  ```python
  from django.core.mail import send_mail

  send_mail(
      'Teste Sistema Avaí',
      'Email de teste funcionando!',
      'noreply@votacao.avaifc.com.br',
      ['admin@avaifc.com.br'],
      fail_silently=False,
  )
  ```
- [ ] **Executar teste** (`python manage.py shell < test_email.py`)

### 9.2 Templates de Email HTML
**Status**: ⏳ Pendente
**Tempo Estimado**: 1 dia

#### 9.2.1 Estrutura de Templates
- [ ] **Criar diretório** `templates/emails/`
- [ ] **Criar template base** `base.html`:
  ```html
  <!DOCTYPE html>
  <html>
  <head>
      <meta charset="utf-8">
      <style>
          body { font-family: Arial, sans-serif; }
          .header { background: #1e3a8a; color: white; padding: 20px; }
          .content { padding: 20px; }
          .footer { background: #f3f4f6; padding: 20px; font-size: 12px; }
      </style>
  </head>
  <body>
      <div class="header">
          <h1>Sistema de Votação Avaí FC</h1>
      </div>
      <div class="content">
          {% block content %}{% endblock %}
      </div>
      <div class="footer">
          <p>Este é um email automático. Não responda.</p>
          <p><a href="{% url 'accounts:unsubscribe' %}">Cancelar inscrição</a></p>
      </div>
  </body>
  </html>
  ```

#### 9.2.2 Template de Boas-vindas
- [ ] **Criar** `welcome.html`:
  ```html
  {% extends "emails/base.html" %}

  {% block content %}
  <h2>Bem-vindo ao Sistema de Votação!</h2>
  <p>Olá {{ user.first_name }},</p>
  <p>Seu cadastro foi realizado com sucesso!</p>
  <p>Agora você pode participar das votações do Conselho Deliberativo.</p>
  <a href="{{ login_url }}">Acessar Sistema</a>
  {% endblock %}
  ```

#### 9.2.3 Template de Nova Votação
- [ ] **Criar** `new_voting.html`:
  ```html
  {% extends "emails/base.html" %}

  {% block content %}
  <h2>Nova Votação Disponível</h2>
  <p>Uma nova votação foi criada: <strong>{{ voting.title }}</strong></p>
  <p>Prazo: {{ voting.start_date }} até {{ voting.end_date }}</p>
  <a href="{{ voting_url }}">Participar da Votação</a>
  {% endblock %}
  ```

#### 9.2.4 Template de Lembrete
- [ ] **Criar** `reminder.html`:
  ```html
  {% extends "emails/base.html" %}

  {% block content %}
  <h2>Lembrete: Votação Terminando</h2>
  <p>A votação "{{ voting.title }}" termina em 24 horas!</p>
  <p>Não perca a chance de votar.</p>
  <a href="{{ voting_url }}">Votar Agora</a>
  {% endblock %}
  ```

### 9.3 Sistema de Notificações
**Status**: ⏳ Pendente
**Tempo Estimado**: 1 dia

#### 9.3.1 Signals para Notificações
- [ ] **Criar arquivo** `business/signals.py`:
  ```python
  from django.db.models.signals import post_save
  from django.dispatch import receiver
  from django.core.mail import send_mail
  from .models import Voting, Vote

  @receiver(post_save, sender=Voting)
  def notify_new_voting(sender, instance, created, **kwargs):
      if created:
          # Enviar email para todos os usuários
          from django.contrib.auth.models import User
          users = User.objects.filter(is_active=True)

          for user in users:
              send_mail(
                  f'Nova votação: {instance.title}',
                  f'Nova votação disponível até {instance.end_date}',
                  'noreply@votacao.avaifc.com.br',
                  [user.email],
              )

  @receiver(post_save, sender=Vote)
  def notify_vote_confirmation(sender, instance, created, **kwargs):
      if created:
          send_mail(
              'Voto confirmado',
              f'Seu voto em "{instance.voting.title}" foi registrado.',
              'noreply@votacao.avaifc.com.br',
              [instance.user.email],
          )
  ```

#### 9.3.2 Comando de Lembretes
- [ ] **Criar comando** `business/management/commands/send_reminders.py`:
  ```python
  from django.core.management.base import BaseCommand
  from django.utils import timezone
  from business.models import Voting
  from django.core.mail import send_mail

  class Command(BaseCommand):
      help = 'Send voting reminders'

      def handle(self, *args, **options):
          tomorrow = timezone.now() + timezone.timedelta(days=1)
          votings = Voting.objects.filter(
              end_date__date=tomorrow.date(),
              is_active=True
          )

          for voting in votings:
              # Enviar lembretes para usuários que ainda não votaram
              voted_users = voting.votes.values_list('user', flat=True)
              users_to_remind = voting.presences.filter(
                  present=True
              ).exclude(user__in=voted_users)

              for presence in users_to_remind:
                  send_mail(
                      f'Lembrete: Votação termina amanhã',
                      f'A votação "{voting.title}" termina amanhã!',
                      'noreply@votacao.avaifc.com.br',
                      [presence.user.email],
                  )
  ```

#### 9.3.3 Agendamento de Lembretes
- [ ] **Adicionar ao crontab**:
  ```
  # Lembretes diários às 9:00 AM
  0 9 * * * /opt/avai-voting/venv/bin/python /opt/avai-voting/manage.py send_reminders
  ```

#### 9.3.4 Sistema de Opt-out
- [ ] **Adicionar campo** `email_notifications` ao modelo User
- [ ] **Criar view** de unsubscribe
- [ ] **Atualizar templates** para incluir link de opt-out

---

## 🎯 SPRINT 10: QUALIDADE E AUTOMAÇÃO
**Duração Estimada**: 6-8 dias
**Prioridade**: 🟢 Baixa

### 10.1 Testes Automatizados - Unitários
**Status**: ⏳ Pendente
**Tempo Estimado**: 2 dias

#### 10.1.1 Configuração do Ambiente de Testes
- [ ] **Adicionar ao requirements.txt**:
  ```
  pytest==7.4.3
  pytest-django==4.7.0
  coverage==7.3.2
  factory-boy==3.3.0
  ```
- [ ] **Criar arquivo** `pytest.ini`:
  ```ini
  [tool:pytest]
  DJANGO_SETTINGS_MODULE = core.settings
  python_files = test_*.py
  addopts = --cov=. --cov-report=html
  ```

#### 10.1.2 Fixtures e Factories
- [ ] **Criar arquivo** `tests/conftest.py`:
  ```python
  import pytest
  from django.contrib.auth.models import User
  from business.models import Meeting, Presence, Voting, VotingOption

  @pytest.fixture
  def user():
      return User.objects.create_user(
          username='testuser',
          email='test@example.com',
          password='testpass123'
      )

  @pytest.fixture
  def meeting():
      return Meeting.objects.create(
          title='Reunião de Teste',
          meeting_date='2024-01-01'
      )
  ```

#### 10.1.3 Testes de Models
- [ ] **Criar arquivo** `tests/unit/test_models.py`:
  ```python
  import pytest
  from business.models import Meeting, Presence, Voting

  @pytest.mark.django_db
  class TestMeeting:
      def test_meeting_creation(self):
          meeting = Meeting.objects.create(
              title='Test Meeting',
              meeting_date='2024-01-01'
          )
          assert meeting.title == 'Test Meeting'
          assert str(meeting) == 'Test Meeting - 2024-01-01 (Ativa)'

      def test_total_presences(self, meeting, user):
          Presence.objects.create(meeting=meeting, user=user, present=True)
          assert meeting.total_presences() == 1

  @pytest.mark.django_db
  class TestPresence:
      def test_presence_creation(self, meeting, user):
          presence = Presence.objects.create(
              meeting=meeting,
              user=user,
              present=True
          )
          assert presence.present == True
          assert str(presence) == f'{user.username} - {meeting.title} ({meeting.meeting_date})'
  ```

#### 10.1.4 Testes de Utils
- [ ] **Criar arquivo** `tests/unit/test_utils.py`:
  ```python
  import pytest
  from business.utils import PresencePDFExporter
  from io import BytesIO

  @pytest.mark.django_db
  class TestPresencePDFExporter:
      def test_pdf_generation(self, meeting, user):
          queryset = Presence.objects.filter(meeting=meeting)
          exporter = PresencePDFExporter(queryset)

          buffer = BytesIO()
          exporter.generate_pdf(buffer)

          # Verificar se PDF foi gerado
          assert buffer.tell() > 0
  ```

### 10.2 Testes de Integração
**Status**: ⏳ Pendente
**Tempo Estimado**: 2 dias

#### 10.2.1 Testes de Views
- [ ] **Criar arquivo** `tests/integration/test_views.py`:
  ```python
  import pytest
  from django.test import Client
  from django.urls import reverse

  @pytest.mark.django_db
  class TestVotingViews:
      def test_voting_list_view(self, client, user):
          client.login(username=user.username, password='testpass123')
          response = client.get(reverse('business:voting_list'))
          assert response.status_code == 200

      def test_voting_creation_requires_staff(self, client, user):
          client.login(username=user.username, password='testpass123')
          response = client.get(reverse('business:voting_create'))
          assert response.status_code == 403  # Forbidden
  ```

#### 10.2.2 Testes de Forms
- [ ] **Criar arquivo** `tests/integration/test_forms.py`:
  ```python
  import pytest
  from business.forms import VotingForm

  @pytest.mark.django_db
  class TestVotingForm:
      def test_valid_form(self, user):
          form_data = {
              'title': 'Test Voting',
              'description': 'Test Description',
              'start_date': '2024-01-01 10:00:00',
              'end_date': '2024-01-02 10:00:00',
              'requires_presence': True,
          }
          form = VotingForm(data=form_data)
          form.instance.created_by = user
          assert form.is_valid()

      def test_end_before_start_invalid(self, user):
          form_data = {
              'title': 'Test Voting',
              'start_date': '2024-01-02 10:00:00',
              'end_date': '2024-01-01 10:00:00',  # End before start
          }
          form = VotingForm(data=form_data)
          form.instance.created_by = user
          assert not form.is_valid()
  ```

### 10.3 Testes End-to-End
**Status**: ⏳ Pendente
**Tempo Estimado**: 2 dias

#### 10.3.1 Configuração Selenium
- [ ] **Instalar Chrome Driver**:
  ```bash
  wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | sudo apt-key add -
  echo 'deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main' | sudo tee /etc/apt/sources.list.d/google-chrome.list
  sudo apt update
  sudo apt install google-chrome-stable
  ```

- [ ] **Adicionar ao requirements.txt**:
  ```
  selenium==4.16.0
  webdriver-manager==4.0.1
  ```

#### 10.3.2 Testes E2E
- [ ] **Criar arquivo** `tests/e2e/test_voting_flow.py`:
  ```python
  import pytest
  from selenium import webdriver
  from selenium.webdriver.common.by import By
  from selenium.webdriver.support.ui import WebDriverWait
  from selenium.webdriver.support import expected_conditions as EC

  @pytest.fixture
  def browser():
      driver = webdriver.Chrome()
      yield driver
      driver.quit()

  class TestVotingFlow:
      def test_complete_voting_flow(self, browser, live_server):
          browser.get(live_server.url + '/accounts/login/')

          # Login
          browser.find_element(By.NAME, 'username').send_keys('admin')
          browser.find_element(By.NAME, 'password').send_keys('admin123')
          browser.find_element(By.CSS_SELECTOR, 'input[type="submit"]').click()

          # Verificar login
          WebDriverWait(browser, 10).until(
              EC.presence_of_element_located((By.LINK_TEXT, "Dashboard"))
          )

          # Ir para votações
          browser.find_element(By.LINK_TEXT, "Votações").click()

          # Verificar página de votações
          assert "Votações Ativas" in browser.page_source
  ```

### 10.4 CI/CD Pipeline
**Status**: ⏳ Pendente
**Tempo Estimado**: 2-3 dias

#### 10.4.1 Configuração GitHub Actions
- [ ] **Criar arquivo** `.github/workflows/ci.yml`:
  ```yaml
  name: CI/CD Pipeline

  on:
    push:
      branches: [ main, develop ]
    pull_request:
      branches: [ main ]

  jobs:
    test:
      runs-on: ubuntu-latest

      services:
        postgres:
          image: postgres:15
          env:
            POSTGRES_PASSWORD: postgres
          options: >-
            --health-cmd pg_isready
            --health-interval 10s
            --health-timeout 5s
            --health-retries 5

      steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt

      - name: Run tests
        run: pytest --cov=. --cov-report=xml

      - name: Upload coverage
        uses: codecov/codecov-action@v3
        with:
          file: ./coverage.xml
  ```

#### 10.4.2 Configuração de Linting
- [ ] **Adicionar ao requirements.txt**:
  ```
  black==23.12.1
  flake8==7.0.0
  isort==5.13.2
  mypy==1.8.0
  ```

- [ ] **Criar arquivo** `pyproject.toml`:
  ```toml
  [tool.black]
  line-length = 88
  target-version = ['py311']

  [tool.isort]
  profile = "black"
  ```

- [ ] **Atualizar CI** para incluir linting:
  ```yaml
  - name: Lint code
    run: |
      black --check .
      isort --check-only .
      flake8 .
  ```

#### 10.4.3 Deploy Automático
- [ ] **Adicionar job de deploy**:
  ```yaml
  deploy:
    runs-on: ubuntu-latest
    needs: test
    if: github.ref == 'refs/heads/main'

    steps:
    - name: Deploy to production
      run: |
        echo "Deploy to production server"
        # Adicionar comandos de deploy via SSH
  ```

#### 10.4.4 Configuração de Secrets
- [ ] **Adicionar secrets no GitHub**:
  - `PRODUCTION_HOST`
  - `PRODUCTION_USER`
  - `SSH_PRIVATE_KEY`
  - `DATABASE_URL`

---

## 📊 Métricas de Acompanhamento

### Checklist Geral de Qualidade
- [ ] **Cobertura de Testes**: > 80%
- [ ] **Tempo de Build**: < 5 minutos
- [ ] **Tempo de Testes**: < 3 minutos
- [ ] **Complexidade Ciclomática**: < 10
- [ ] **Dívida Técnica**: < 5% do código

### Métricas por Sprint
- **Sprint 7**: Infraestrutura operacional
- **Sprint 8**: Exports funcionando
- **Sprint 9**: Notificações ativas
- **Sprint 10**: Pipeline CI/CD ativo

---

**Lista de tarefas criada para desenvolvimento futuro**  
**Total de tarefas**: 80+ subtarefas granulares  
**Estimativa total**: 14-19 dias  
**Status**: ⏳ Pronto para desenvolvimento futuro</content>
<parameter name="filePath">/mnt/extra60gb/Documentos/sistema_votacao/TASKLIST_FUTURO.md
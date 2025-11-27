# Estrutura de Apps

## Visão Geral

O projeto segue a arquitetura modular do Django, separando funcionalidades em apps isolados. Cada app é responsável por um domínio específico do sistema.

## Apps do Projeto

### 1. accounts
**Responsabilidade**: Gerenciamento de usuários e autenticação

**Funcionalidades planejadas:**
- Login/Logout de usuários
- Cadastro de novos usuários
- Perfil de usuário
- Autenticação via username

**Estrutura:**
```
accounts/
├── __init__.py
├── admin.py          # Configuração do Django Admin
├── apps.py           # Configuração do app
├── models.py         # Models customizados (se necessário)
├── views.py          # Views de autenticação
├── urls.py           # URLs do app
├── forms.py          # Forms de login/cadastro
└── templates/
    └── accounts/
        ├── login.html
        └── register.html
```

### 2. business
**Responsabilidade**: Lógica de negócio principal (votações e presença)

**Funcionalidades planejadas:**
- Controle de presença em reuniões
- Criação e gerenciamento de votações
- Opções de votação editáveis
- Registro de votos

**Models esperados:**
- `Presence`: Controle de presença
- `Voting`: Votações
- `VotingOption`: Opções de voto
- `Vote`: Votos registrados

**Estrutura:**
```
business/
├── __init__.py
├── admin.py
├── apps.py
├── models.py         # Models de votação e presença
├── views.py          # Views de negócio
├── urls.py
├── forms.py          # Forms de votação
└── templates/
    └── business/
        ├── voting_list.html
        ├── voting_create.html
        └── voting_vote.html
```

### 3. performance
**Responsabilidade**: Métricas e análise de performance

**Funcionalidades planejadas:**
- Coleta de métricas do sistema
- Análise de uso
- Monitoramento de votações

**Estrutura:**
```
performance/
├── __init__.py
├── admin.py
├── apps.py
├── models.py         # Models de métricas
├── views.py
└── templates/
    └── performance/
```

### 4. scouting
**Responsabilidade**: Relatórios e visualizações

**Funcionalidades planejadas:**
- Relatório de presença
- Relatório de votações
- Lista de votantes por opção
- Exportação de dados

**Estrutura:**
```
scouting/
├── __init__.py
├── admin.py
├── apps.py
├── models.py
├── views.py          # Views de relatórios
├── urls.py
└── templates/
    └── scouting/
        ├── report_presence.html
        └── report_voting.html
```

### 5. core
**Responsabilidade**: Configurações centrais do Django

**Arquivos:**
- `settings.py`: Configurações do projeto
- `urls.py`: URLs principais
- `wsgi.py`: Configuração WSGI
- `asgi.py`: Configuração ASGI

## Convenções

### Criação de Novo App

1. Criar app:
```bash
python manage.py startapp nome_do_app
```

2. Adicionar em `INSTALLED_APPS` no `settings.py`

3. Criar estrutura de templates:
```
nome_do_app/templates/nome_do_app/
```

4. Criar `urls.py` no app

5. Incluir URLs no `core/urls.py`

### Models
- Todos os models devem herdar de `models.Model`
- Incluir campos `created_at` e `updated_at`
- Definir `Meta` class com `verbose_name`
- Implementar método `__str__()`

### Views
- Preferir Class Based Views
- Usar generic views quando possível
- Nomear views de forma descritiva: `ExampleListView`, `ExampleCreateView`

### Templates
- Organizar por app: `app/templates/app/template.html`
- Usar naming com underscore: `example_list.html`
- Herdar de `base.html`

### URLs
- Definir `app_name` em cada `urls.py`
- Usar `name` em todas as rotas para reverse URLs
- Padrão: `path('rota/', views.ViewName.as_view(), name='nome')`

## Comunicação Entre Apps

### Imports
```python
# Correto
from business.models import Voting
from accounts.models import User

# Evitar imports circulares
```

### Signals
- Usar signals para comunicação entre apps
- Criar arquivo `signals.py` no app emissor
- Registrar no `apps.py`

```python
# business/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Vote

@receiver(post_save, sender=Vote)
def update_voting_count(sender, instance, created, **kwargs):
    if created:
        # Lógica após criar voto
        pass
```

## Boas Práticas

- **Um app = Uma responsabilidade**
- **Evitar dependências circulares**
- **Manter apps independentes quando possível**
- **Usar signals para comunicação assíncrona**
- **Documentar dependências entre apps**

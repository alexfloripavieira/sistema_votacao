# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Comandos de Build/Lint/Test

```bash
# Ativar ambiente virtual (sempre primeiro)
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Executar servidor de desenvolvimento
python manage.py runserver

# Executar migrações
python manage.py makemigrations
python manage.py migrate

# Criar superusuário
python manage.py createsuperuser

# Testes (quando implementados)
python manage.py test
python manage.py test app_name.tests.TestClassName.test_method_name  # Teste específico

# Acessar sistema
# App: http://localhost:8000
# Admin: http://localhost:8000/admin
```

## Arquitetura do Projeto

### Apps e Responsabilidades

**Sistema de Votação Eletrônica para o Conselho Deliberativo do Avaí FC**

- **accounts/**: Autenticação e dashboard
  - Login/logout/registro de usuários
  - Dashboard com visualização diferenciada (staff vs usuário comum)
  - Usa Class Based Views: `CustomLoginView`, `RegisterView`, `DashboardView`

- **business/**: Domínio principal (votações e presenças)
  - **Meetings**: Sistema de reuniões (iniciar/encerrar)
  - **Presence**: Controle de presença vinculado a reuniões
  - **Voting**: Sistema completo de votações com opções (A, B, C...)
  - **Reports**: Relatórios administrativos de presença e votação
  - Todas as views usam CBVs com mixins apropriados

### Fluxo Crítico: Meeting → Presence → Voting

1. Admin inicia uma reunião (`Meeting`) com data específica
2. Sistema cria registros de `Presence` para todos os usuários (inicialmente `present=False`)
3. Admin marca presença via interface administrativa ou usuários marcam presença própria
4. Usuários com presença marcada podem votar em votações que requerem presença
5. Admin pode encerrar reunião quando finalizada

### Models e Relacionamentos

- `Meeting` (1) → (N) `Presence` → (N) `User`
- `Voting` (1) → (N) `VotingOption` (letras A, B, C...)
- `Vote` → FK para `User`, `Voting`, `VotingOption` (unique_together: user + voting)
- Todos os models têm `created_at` e `updated_at` (obrigatório)

## Padrões de Código

### Idioma
- **Código**: Inglês (variáveis, funções, classes, comentários)
- **UI/Templates**: Português brasileiro

### Formatação
- **Aspas**: Sempre usar aspas simples `'` (nunca duplas `"`)
- **PEP 8**: Seguir estritamente (4 espaços, max 79 caracteres/linha)
- **Imports**: `from django.db import models` (ordem: stdlib, third-party, local)

### Django Models
```python
class ExampleModel(models.Model):
    name = models.CharField('Nome', max_length=100)
    created_at = models.DateTimeField('Criado em', auto_now_add=True)  # Obrigatório
    updated_at = models.DateTimeField('Atualizado em', auto_now=True)  # Obrigatório
    
    class Meta:
        verbose_name = 'Exemplo'
        verbose_name_plural = 'Exemplos'
    
    def __str__(self):
        return self.name
```

### Views
- **Preferir Class Based Views**: `ListView`, `DetailView`, `CreateView`, etc.
- Exemplo: `class ExampleListView(ListView): ...`
- **Permissões**: Usar `LoginRequiredMixin` e `UserPassesTestMixin`
  ```python
  class AdminOnlyView(LoginRequiredMixin, UserPassesTestMixin, ListView):
      def test_func(self):
          return self.request.user.is_staff
  ```
- **Query Optimization**: SEMPRE usar `select_related()` e `prefetch_related()`
  ```python
  # Exemplo do projeto
  queryset = Presence.objects.select_related('user', 'meeting')
  votings = Voting.objects.prefetch_related('options')
  ```

### Templates
- Naming: `app_name/templates/app_name/template_name.html`
- Sempre usar `{% extends 'base.html' %}` e `{% block content %}`
- Dashboard tem templates separados: `dashboard_admin.html` vs `dashboard_user.html`

### URLs
- Definir `app_name` em cada `urls.py`
- Usar `name` em todas as rotas: `path('', views.View.as_view(), name='list')`

### Signals
- Criar `signals.py` dentro do app
- Registrar no `apps.py` método `ready()`

### Cache
- Usar Django local memory cache para estatísticas
- **Timeouts padrão**: 300s (5min) para stats, 600s (10min) para agregações
- **Padrão de uso**:
  ```python
  from django.core.cache import cache

  cache_key = f'stats_{date}'
  cached_data = cache.get(cache_key)
  if not cached_data:
      cached_data = expensive_query()
      cache.set(cache_key, cached_data, 300)
  ```

### Transações
- Usar `transaction.atomic()` para operações que atualizam múltiplos objetos
- Exemplo: votar atualiza `Vote` e `VotingOption.votes_count`

### AJAX Views
- Views que retornam JSON devem usar `JsonResponse`
- Exemplo: `TogglePresenceView` retorna `{'success': True, 'message': '...'}`

## Design System (TailwindCSS)

### Paleta de Cores Oficial do Avaí FC
- **Azul Avaí**: `#006EB6` - Cor principal (botões primários, destaques, links)
- **Azul Avaí Dark**: `#005490` - Hover de botões primários
- **Azul Avaí Darker**: `#003d6b` - Backgrounds escuros e elementos secundários
- **Azul Avaí Light**: `#0088E0` - Botões secundários, elementos de destaque alternativos
- **Branco Avaí**: `#FFFFFF` - Textos em fundos escuros

### Classes Tailwind Customizadas
```javascript
// Configuração no base.html
tailwind.config = {
    theme: {
        extend: {
            colors: {
                'avai-blue': '#006EB6',
                'avai-blue-dark': '#005490',
                'avai-blue-darker': '#003d6b',
                'avai-blue-light': '#0088E0',
                'avai-white': '#FFFFFF',
            }
        }
    }
}
```

### Uso das Cores
- **Backgrounds**: `bg-gray-900`, `bg-gray-800` (fundos principais), `bg-avai-blue` (destaques)
- **Textos**: `text-white`, `text-gray-300`, `text-avai-blue-light`
- **Gradiente**: `bg-gradient-to-br from-gray-900 to-gray-800`
- **Botões Primários**: `bg-avai-blue hover:bg-avai-blue-dark text-white rounded-lg px-4 py-2`
- **Botões Secundários**: `bg-avai-blue-light hover:bg-avai-blue text-white rounded-lg px-4 py-2`
- **Inputs**: `border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-avai-blue bg-gray-700 text-white`
- **Bordas de destaque**: `border-avai-blue` (elementos selecionados)
- **Status**: Manter `bg-red-600` (erros), `bg-yellow-600` (avisos)

## Configurações Importantes (settings.py)

```python
# Autenticação
LOGIN_URL = 'accounts:login'
LOGIN_REDIRECT_URL = 'dashboard'
LOGOUT_REDIRECT_URL = 'home'

# Internacionalização
LANGUAGE_CODE = 'pt-br'
TIME_ZONE = 'America/Sao_Paulo'

# Cache - Local Memory
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'TIMEOUT': 300,  # 5 minutos
    }
}

# Installed Apps
INSTALLED_APPS = [
    # ...
    'accounts',   # Autenticação e dashboard
    'business',   # Votações, presenças, reuniões, relatórios
]
```

## Princípios
- **Não fazer over-engineering** - Mantenha simples
- **Django Way** - Use recursos nativos do Django
- **Apps isolados** - Cada domínio em um app separado
- **SQLite** - Banco de dados padrão
- **Otimização de queries** - Sempre use select_related/prefetch_related
- **Segurança** - Validar permissões, presença antes de votar, unique constraints

# CLAUDE.md - Guia para Agentes de IA

## Comandos de Build/Lint/Test
```bash
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
```

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

### Templates
- Naming: `app_name/templates/app_name/template_name.html`
- Sempre usar `{% extends 'base.html' %}` e `{% block content %}`

### URLs
- Definir `app_name` em cada `urls.py`
- Usar `name` em todas as rotas: `path('', views.View.as_view(), name='list')`

### Signals
- Criar `signals.py` dentro do app
- Registrar no `apps.py` método `ready()`

## Design System (TailwindCSS)
- **Cores**: `bg-gray-900`, `bg-blue-600`, `text-white`, `text-gray-300`
- **Gradiente**: `bg-gradient-to-br from-gray-900 to-gray-800`
- **Botões**: `bg-blue-600 hover:bg-blue-700 text-white rounded-lg px-4 py-2`
- **Inputs**: `border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-500 bg-gray-800 text-white`

## Princípios
- **Não fazer over-engineering** - Mantenha simples
- **Django Way** - Use recursos nativos do Django
- **Apps isolados** - Cada domínio em um app separado
- **SQLite** - Banco de dados padrão

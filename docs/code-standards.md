# Padrões de Código

## Regras Gerais

### Idioma
- **Código**: Inglês (variáveis, funções, classes, comentários)
- **Interface do Usuário**: Português brasileiro

### Aspas
- **Sempre usar aspas simples** (`'`) em vez de aspas duplas (`"`)
- Exemplo: `from django.db import models` ✓
- Exemplo: `name = 'John Doe'` ✓

### Formatação
- Seguir **PEP 8** estritamente
- Indentação: 4 espaços
- Linha máxima: 79 caracteres
- Linhas em branco: 2 entre classes, 1 entre métodos

## Django Específico

### Models
```python
from django.db import models

class ExampleModel(models.Model):
    name = models.CharField('Nome', max_length=100)
    created_at = models.DateTimeField('Criado em', auto_now_add=True)
    updated_at = models.DateTimeField('Atualizado em', auto_now=True)
    
    class Meta:
        verbose_name = 'Exemplo'
        verbose_name_plural = 'Exemplos'
    
    def __str__(self):
        return self.name
```

**Obrigatório em todos os models:**
- Campos `created_at` e `updated_at`
- `verbose_name` em português nos campos
- `Meta` class com `verbose_name` e `verbose_name_plural`
- Método `__str__()`

### Views
- **Preferir Class Based Views (CBV)** quando possível
- Usar generic views do Django: `ListView`, `DetailView`, `CreateView`, etc.

```python
from django.views.generic import ListView

class ExampleListView(ListView):
    model = ExampleModel
    template_name = 'example_list.html'
    context_object_name = 'examples'
```

### URLs
```python
from django.urls import path
from . import views

app_name = 'example'

urlpatterns = [
    path('', views.ExampleListView.as_view(), name='list'),
]
```

### Signals
- Signals devem ficar em arquivo `signals.py` dentro do app correspondente
- Registrar signals no `apps.py` do app

```python
# apps.py
from django.apps import AppConfig

class ExampleConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'example'
    
    def ready(self):
        import example.signals
```

## Templates

### Estrutura
```django
{% extends 'base.html' %}

{% block title %}Título da Página{% endblock %}

{% block content %}
<div class="container mx-auto px-4">
    <!-- Conteúdo -->
</div>
{% endblock %}
```

### Naming
- Usar underscore para separar palavras: `example_list.html`
- Organizar por app: `templates/example/example_list.html`

## Princípios

- **Simplicidade**: Não fazer over-engineering
- **Django Way**: Usar recursos nativos do Django sempre que possível
- **DRY**: Don't Repeat Yourself
- **KISS**: Keep It Simple, Stupid

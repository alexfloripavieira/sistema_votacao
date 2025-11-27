# Agentes de IA - Sistema de Votação Eletrônica

Este diretório contém os agentes especializados para desenvolvimento do projeto. Cada agente possui expertise específica na stack tecnológica do sistema.

## Índice de Agentes

### 1. [Backend Django](backend-django.md)
**Especialidade**: Python, Django, Models, Views, URLs, Admin
**Quando usar**: 
- Criar/modificar models Django
- Implementar views (CBV)
- Configurar URLs e routing
- Criar signals e business logic
- Configurar Django Admin

### 2. [Frontend Template](frontend-template.md)
**Especialidade**: Django Template Language, TailwindCSS, HTML, Design System
**Quando usar**:
- Criar/modificar templates Django
- Implementar design system com TailwindCSS
- Criar componentes visuais (botões, forms, cards)
- Garantir responsividade mobile
- Implementar layouts e navegação

### 3. [QA/Tester](qa-tester.md)
**Especialidade**: Testes E2E, Playwright, Validação de Design, UX Testing
**Quando usar**:
- Testar fluxos completos do sistema
- Validar design e responsividade
- Verificar funcionalidades implementadas
- Testar diferentes navegadores/dispositivos
- Validar critérios de aceite

### 4. [Database Engineer](database-engineer.md)
**Especialidade**: SQLite, Django ORM, Migrations, Data Modeling
**Quando usar**:
- Criar/modificar estrutura de banco de dados
- Gerenciar migrations
- Otimizar queries e relacionamentos
- Resolver problemas de integridade de dados

### 5. [Integration Engineer](integration-engineer.md)
**Especialidade**: Integração entre Apps, Signals, APIs internas
**Quando usar**:
- Integrar diferentes apps Django
- Implementar comunicação entre módulos
- Criar signals para eventos
- Garantir coesão do sistema

## Fluxo de Trabalho Recomendado

### Para Nova Funcionalidade
1. **Database Engineer** → Criar models
2. **Backend Django** → Implementar views e business logic
3. **Frontend Template** → Criar templates e UI
4. **Integration Engineer** → Conectar componentes
5. **QA/Tester** → Validar funcionalidade completa

### Para Bug Fix
1. **QA/Tester** → Reproduzir e documentar bug
2. **Backend Django** ou **Frontend Template** → Corrigir
3. **QA/Tester** → Validar correção

### Para Melhorias de UI
1. **Frontend Template** → Implementar mudanças
2. **QA/Tester** → Validar visual e responsividade

## Stack do Projeto
- **Backend**: Python 3.x, Django 4.x
- **Frontend**: Django Template Language, TailwindCSS
- **Database**: SQLite
- **Testing**: Playwright (E2E)

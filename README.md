# Sistema de Votação Eletrônica - Avaí FC

Sistema de votação eletrônico desenvolvido para o Conselho Deliberativo do Avaí FC, permitindo votações seguras e eficientes em reuniões com controle de presença, resultados em tempo real e relatórios detalhados.

## 🚀 Tecnologias

- **Backend**: Python 3.x + Django 4.2.26
- **Frontend**: Django Templates + TailwindCSS (via CDN)
- **Banco de Dados**: SQLite
- **Cache**: Django Local Memory Cache
- **Autenticação**: Django Auth (username-based)

## 📋 Funcionalidades

### ✅ Autenticação e Segurança
- Sistema de login e cadastro de usuários
- Autenticação obrigatória para acesso ao sistema
- Controle de permissões (usuários comuns e staff)
- Logout seguro

### ✅ Controle de Presença
- Marcação de presença nas reuniões
- Histórico de presenças
- Lista de presentes em tempo real
- Relatórios de presença por data

### ✅ Sistema de Votações
- Criação de votações com múltiplas opções (A, B, C...)
- Adição/remoção dinâmica de opções
- Validação de presença antes de votar
- Um voto por usuário por votação
- Votações com prazo de início e término
- Status em tempo real (aberta/encerrada)

### ✅ Resultados e Relatórios
- Resultados em tempo real com atualização automática
- Lista detalhada de votantes por opção
- Percentual de votos por opção
- Relatórios administrativos completos
- Dashboard administrativo com estatísticas
- Relatório de presenças com filtros

### ✅ Interface e UX
- Design responsivo (mobile-first)
- Tema escuro moderno
- Cores do Avaí FC (verde #22c55e)
- Interface intuitiva e fácil de usar
- Feedback visual de ações
- Mensagens de sucesso/erro

## 🏗️ Estrutura do Projeto

```
sistema_votacao/
├── accounts/              # App de autenticação
│   ├── views.py          # Views de login, registro, dashboard
│   ├── urls.py           # URLs de autenticação
│   └── templates/        # Templates de auth
├── business/             # App de negócios (votações e presenças)
│   ├── models.py         # Models: Presence, Voting, VotingOption, Vote
│   ├── views.py          # Views de votação e relatórios
│   ├── admin.py          # Configuração do admin
│   ├── urls.py           # URLs do business
│   └── templates/        # Templates de votação
├── core/                 # Configurações do projeto
│   ├── settings.py       # Configurações Django
│   └── urls.py           # URLs principais
├── templates/            # Templates base
│   ├── base.html         # Template base
│   ├── home.html         # Página inicial
│   ├── dashboard.html    # Dashboard do usuário
│   └── includes/         # Componentes reutilizáveis
│       ├── navbar.html
│       └── footer.html
├── manage.py
├── requirements.txt
├── CLAUDE.md            # Guia para agentes de IA
├── PRD.md               # Product Requirement Document
└── README.md            # Este arquivo
```

## 🗄️ Modelos de Dados

### User (Django Auth)
- username, email, password
- first_name, last_name
- is_staff, is_active

### Presence
- user (FK → User)
- meeting_date (Date)
- present (Boolean)
- created_at, updated_at

### Voting
- title, description
- start_date, end_date (DateTime)
- requires_presence (Boolean)
- is_active (Boolean)
- created_by (FK → User)
- created_at, updated_at

### VotingOption
- voting (FK → Voting)
- option_text (CharField)
- option_letter (CharField: A, B, C...)
- votes_count (Integer)
- created_at, updated_at

### Vote
- voting (FK → Voting)
- user (FK → User)
- option (FK → VotingOption)
- voted_at, created_at, updated_at
- UNIQUE(voting, user) - Um voto por usuário

## 🚀 Instalação e Configuração

### Pré-requisitos
- Python 3.8+
- pip

### Passos

1. **Clone o repositório**
```bash
cd /caminho/do/projeto
```

2. **Crie e ative o ambiente virtual**
```bash
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows
```

3. **Instale as dependências**
```bash
pip install -r requirements.txt
```

4. **Execute as migrações**
```bash
python manage.py makemigrations
python manage.py migrate
```

5. **Crie um superusuário**
```bash
python manage.py createsuperuser
```

6. **Execute o servidor**
```bash
python manage.py runserver
```

7. **Acesse o sistema**
- Aplicação: http://localhost:8000
- Admin: http://localhost:8000/admin

## 📱 Uso do Sistema

### Para Usuários Comuns

1. **Primeiro Acesso**
   - Acesse a página inicial
   - Clique em "Cadastre-se"
   - Preencha o formulário de cadastro
   - Faça login com suas credenciais

2. **Marcar Presença**
   - No dashboard, clique em "Presença"
   - Clique no botão "Marcar Presença"
   - Confirmação aparecerá na tela

3. **Votar**
   - No menu, clique em "Votações"
   - Selecione a votação desejada
   - Escolha uma opção (A, B, C...)
   - Clique em "Confirmar Voto"

4. **Ver Resultados**
   - Após votar, clique em "Ver Resultados Detalhados"
   - Veja o percentual de cada opção
   - Veja quem votou em cada opção

### Para Administradores (Staff)

1. **Dashboard Administrativo**
   - Acesse via menu "Admin"
   - Veja estatísticas gerais do sistema
   - Acesse relatórios rápidos

2. **Criar Votação**
   - Dashboard Admin → "Nova Votação"
   - Preencha título e descrição
   - Defina data de início e término
   - Adicione opções (mínimo 2)
   - Marque "Requer Presença" se necessário
   - Salve a votação

3. **Relatórios**
   - **Relatório de Presenças**: Lista completa com filtros por data
   - **Relatório de Votação**: Detalhes completos de uma votação específica
   - **Dashboard Admin**: Visão geral e estatísticas

4. **Painel Django Admin**
   - Acesse /admin/ para gerenciamento completo
   - Gerencie usuários, votações, presenças
   - Visualize todas as opções e votos

## 🎨 Design System

### Cores
- **Primary**: `#1e3a8a` (Blue)
- **Avaí Green**: `#22c55e`
- **Background**: Gradient `from-gray-900 to-gray-800`
- **Cards**: `bg-gray-800` with `border-gray-700`

### Componentes
- **Botões**: Rounded, hover states, transitions
- **Forms**: Gray theme with blue focus rings
- **Cards**: Shadow, border, hover effects
- **Tables**: Striped, responsive, hover rows

## ⚡ Performance

- **Queries Otimizadas**: Uso de `select_related` e `prefetch_related`
- **Cache**: Local memory cache para estatísticas (5-10 min)
- **Paginação**: Implementada em todas as listas
- **Índices**: Unique constraints e foreign keys otimizados

## 🔒 Segurança

- Autenticação obrigatória
- CSRF protection habilitado
- Validação de presença antes de votar
- Um voto por usuário (unique constraint)
- Controle de permissões staff/user
- Validação de datas nas votações

## 🧪 Testes Manuais

### Fluxo Completo
1. ✅ Cadastro de novo usuário
2. ✅ Login com credenciais
3. ✅ Marcar presença
4. ✅ Criar votação (staff)
5. ✅ Visualizar votações ativas
6. ✅ Votar em uma votação
7. ✅ Ver resultados em tempo real
8. ✅ Gerar relatórios (staff)
9. ✅ Logout

### Casos de Teste
- ✅ Tentar votar sem presença (deve bloquear)
- ✅ Tentar votar duas vezes (deve bloquear)
- ✅ Votar em votação encerrada (deve bloquear)
- ✅ Criar votação com menos de 2 opções (deve validar)
- ✅ Criar votação com data fim < data início (deve validar)

## 📊 Estatísticas

- Total de votações criadas
- Votações ativas no momento
- Total de votos registrados
- Presenças do dia
- Votantes mais ativos
- Histórico de presenças

## 🚀 Próximos Passos (Futuro)

- [ ] Export de relatórios para PDF/Excel
- [ ] Notificações por email
- [ ] Votações com anexos/imagens
- [ ] Sistema de comentários
- [ ] Votações secretas (opcional)
- [ ] App mobile nativo
- [ ] Integração com API externa

## 📝 Licença

Este projeto foi desenvolvido para uso exclusivo do Conselho Deliberativo do Avaí FC.

## 👥 Contribuindo

Para contribuir com o projeto:

1. Leia o arquivo `CLAUDE.md` para entender os padrões
2. Siga as convenções de código (PEP 8)
3. Use aspas simples `'` (nunca duplas)
4. Código em inglês, UI em português
5. Teste localmente antes de commitar

## 🐛 Reportar Problemas

Para reportar bugs ou sugerir melhorias:
- Descreva o problema detalhadamente
- Inclua passos para reproduzir
- Inclua screenshots se aplicável
- Mencione navegador e versão (se relevante)

## 📞 Suporte

Para questões ou suporte:
- Consulte este README primeiro
- Verifique o arquivo `PRD.md` para requisitos
- Consulte o arquivo `CLAUDE.md` para padrões de código

---

**Desenvolvido para o Avaí Futebol Clube** 💚💙🦅

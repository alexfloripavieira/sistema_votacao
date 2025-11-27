# Como Começar

## Pré-requisitos

- Python 3.x
- pip (gerenciador de pacotes Python)

## Instalação

1. Clone o repositório (quando disponível)

2. Instale as dependências:
```bash
pip install -r requirements.txt
```

3. Execute as migrações do banco de dados:
```bash
python manage.py migrate
```

4. Crie um superusuário:
```bash
python manage.py createsuperuser
```

5. Inicie o servidor de desenvolvimento:
```bash
python manage.py runserver
```

6. Acesse o sistema em `http://localhost:8000`

## Próximos Passos

- Familiarize-se com a [Estrutura de Apps](apps-structure.md)
- Leia os [Padrões de Código](code-standards.md) antes de desenvolver
- Consulte o [Design System](design-system.md) ao criar interfaces

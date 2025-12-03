# Como Configurar o Envio de Email

O sistema está configurado para modo **desenvolvimento** por padrão, onde os emails são impressos no terminal/console ao invés de serem enviados.

## Modo Atual (Desenvolvimento)

```python
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
```

Quando você cadastra um conselheiro, o email aparece no terminal onde o servidor Django está rodando.

---

## Configurar para Produção (Envio Real de Emails)

### Opção 1: Gmail

1. **Abra o arquivo** `core/settings.py`

2. **Comente a linha do console backend**:
   ```python
   # EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
   ```

3. **Descomente e configure as linhas SMTP**:
   ```python
   EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
   EMAIL_HOST = 'smtp.gmail.com'
   EMAIL_PORT = 587
   EMAIL_USE_TLS = True
   EMAIL_HOST_USER = 'seu-email@gmail.com'
   EMAIL_HOST_PASSWORD = 'sua-senha-de-app'
   DEFAULT_FROM_EMAIL = 'Sistema de Votação Avaí FC <seu-email@gmail.com>'
   ```

4. **Criar senha de app do Gmail**:
   - Acesse: https://myaccount.google.com/apppasswords
   - Faça login na conta Gmail
   - Selecione "App: Email" e "Dispositivo: Outro"
   - Digite "Sistema Votação Avaí"
   - Copie a senha gerada (16 caracteres)
   - Cole em `EMAIL_HOST_PASSWORD`

### Opção 2: Outlook/Hotmail

```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp-mail.outlook.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'seu-email@outlook.com'
EMAIL_HOST_PASSWORD = 'sua-senha'
DEFAULT_FROM_EMAIL = 'Sistema de Votação Avaí FC <seu-email@outlook.com>'
```

### Opção 3: Servidor SMTP Próprio

```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.seudominio.com.br'
EMAIL_PORT = 587  # ou 465 para SSL
EMAIL_USE_TLS = True  # ou EMAIL_USE_SSL = True
EMAIL_HOST_USER = 'noreply@seudominio.com.br'
EMAIL_HOST_PASSWORD = 'sua-senha'
DEFAULT_FROM_EMAIL = 'Sistema de Votação Avaí FC <noreply@seudominio.com.br>'
```

---

## Testando o Envio de Email

Após configurar, teste com este comando no terminal:

```bash
source venv/bin/activate
python manage.py shell
```

Dentro do shell do Django:

```python
from django.core.mail import send_mail

send_mail(
    'Teste de Email',
    'Este é um email de teste do sistema.',
    'seu-email@gmail.com',
    ['email-destino@exemplo.com'],
    fail_silently=False,
)
```

Se não houver erro, o email foi enviado com sucesso!

---

## Segurança - NUNCA commitar senhas

**IMPORTANTE**: Nunca coloque senhas reais diretamente no código!

Para produção, use variáveis de ambiente:

1. **Instale python-decouple**:
   ```bash
   pip install python-decouple
   ```

2. **Crie arquivo `.env`** na raiz do projeto:
   ```
   EMAIL_HOST_USER=seu-email@gmail.com
   EMAIL_HOST_PASSWORD=sua-senha-de-app
   ```

3. **Adicione `.env` no `.gitignore`**:
   ```
   .env
   ```

4. **Use no `settings.py`**:
   ```python
   from decouple import config

   EMAIL_HOST_USER = config('EMAIL_HOST_USER')
   EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')
   ```

---

## Resumo do Fluxo de Cadastro

1. **Admin cadastra conselheiro** → Sistema gera senha temporária
2. **Sistema tenta enviar email** → Se configurado, envia; senão, apenas mostra no terminal
3. **Senha aparece na tela** → Admin pode copiar e enviar manualmente
4. **Página "Senhas Temporárias"** → Admin pode consultar senhas de usuários pendentes
5. **Conselheiro faz login** → Middleware força mudança de senha
6. **Nova senha definida** → Acesso liberado, senha temporária é apagada

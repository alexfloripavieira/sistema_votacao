# Como Testar o Envio de Emails

## 🎯 Modo Atual: CONSOLE (Desenvolvimento)

Os emails **NÃO são enviados de verdade**. Eles aparecem no **terminal/console** onde o servidor Django está rodando.

---

## 📝 Passo a Passo para Testar

### Teste 1: Comando de Teste de Email

```bash
# Ative o ambiente virtual
source venv/bin/activate

# Execute o comando de teste
python manage.py testar_email --email seu@email.com
```

**O que vai acontecer:**
- Uma mensagem de cabeçalho explicativa aparece
- O email completo é exibido no terminal
- Mostra se foi sucesso ou erro

---

### Teste 2: Cadastrar um Conselheiro

#### **Etapa 1: Abra o terminal e rode o servidor**

```bash
source venv/bin/activate
python manage.py runserver
```

⚠️ **IMPORTANTE**: Deixe este terminal ABERTO e VISÍVEL durante o cadastro!

#### **Etapa 2: Acesse o sistema**

1. Abra o navegador em: `http://localhost:8000`
2. Faça login como admin
3. Clique em "Cadastrar Conselheiro"
4. Preencha o formulário e clique em "Cadastrar"

#### **Etapa 3: Olhe no TERMINAL onde o servidor está rodando**

Você verá algo assim:

```
============================================================
📧 TENTANDO ENVIAR EMAIL
============================================================
Backend: django.core.mail.backends.console.EmailBackend
De: noreply@avai.com.br
Para: conselheiro@email.com
Assunto: Bem-vindo ao Sistema de Votação do Avaí FC
✓ Email enviado/exibido com sucesso!
============================================================

Content-Type: text/plain; charset="utf-8"
MIME-Version: 1.0
Content-Transfer-Encoding: 7bit
Subject: Bem-vindo ao Sistema de Votação do Avaí FC
From: noreply@avai.com.br
To: conselheiro@email.com
Date: Wed, 03 Dec 2025 19:30:00 -0000
Message-ID: <...>

Olá João da Silva,

Seu cadastro no Sistema de Votação do Conselho Deliberativo do Avaí FC foi realizado com sucesso!

Suas credenciais de acesso são:

Nome de Usuário: joao.silva
Senha Temporária: aB3dE5gH7jK9

IMPORTANTE: Por segurança, você será obrigado a alterar esta senha no primeiro acesso ao sistema.

Para acessar o sistema, visite: http://localhost:8000/

Atenciosamente,
Sistema de Votação Avaí FC

-----------------------------------------------------------------
```

---

## ❌ Se Não Ver o Email no Terminal

### Possíveis Causas:

1. **Terminal está em outra aba/janela**
   - Volte para o terminal onde rodou `python manage.py runserver`

2. **Servidor não está rodando**
   - Verifique se o servidor está ativo
   - Execute novamente: `python manage.py runserver`

3. **Erro no envio**
   - Você verá uma mensagem de erro no terminal
   - A interface web mostrará: "Email não foi enviado: [erro]"

4. **Backend incorreto**
   - Verifique `core/settings.py`
   - Deve ter: `EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'`

---

## ✅ Verificação Rápida

Execute este comando para verificar a configuração:

```bash
python manage.py shell -c "from django.conf import settings; print('Backend:', settings.EMAIL_BACKEND)"
```

Deve retornar:
```
Backend: django.core.mail.backends.console.EmailBackend
```

---

## 📧 Quer Enviar Emails de VERDADE?

### Opção 1: Modo Arquivo (para testes sem internet)

Adicione em `core/settings.py`:

```python
EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
EMAIL_FILE_PATH = BASE_DIR / 'sent_emails'
```

Os emails serão salvos como arquivos na pasta `sent_emails/`

### Opção 2: Gmail Real

Veja o arquivo `CONFIGURAR_EMAIL.md` para instruções completas.

---

## 🐛 Debug

Se ainda não funcionar, execute:

```bash
python manage.py testar_email 2>&1 | tee teste_email.log
```

Isso salva toda a saída no arquivo `teste_email.log` para análise.

---

## 📸 Exemplo Visual

```
┌─────────────────────────────────────────┐
│  NAVEGADOR                              │
│  http://localhost:8000                  │
│                                         │
│  ✓ Conselheiro cadastrado!              │
│  Senha: aB3dE5gH7jK9                   │
│  [Copiar Senha]                         │
└─────────────────────────────────────────┘

                    ↓

┌─────────────────────────────────────────┐
│  TERMINAL (onde o servidor está rodando)│
│                                         │
│  📧 TENTANDO ENVIAR EMAIL               │
│  ============...                        │
│  Backend: console                       │
│  De: noreply@avai.com.br               │
│  Para: conselheiro@email.com            │
│  ✓ Email enviado!                       │
│                                         │
│  [AQUI APARECE O EMAIL COMPLETO]        │
└─────────────────────────────────────────┘
```

---

## 💡 Dica

Para facilitar, rode o servidor em um terminal dedicado que você possa ver enquanto usa o navegador. No Linux/Mac, pode usar tmux ou screen para dividir a tela.

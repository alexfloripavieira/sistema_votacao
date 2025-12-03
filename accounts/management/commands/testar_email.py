from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.conf import settings


class Command(BaseCommand):
    help = 'Testa o envio de email do sistema'

    def add_arguments(self, parser):
        parser.add_argument(
            '--email',
            type=str,
            help='Email de destino para o teste',
            default='teste@exemplo.com'
        )

    def handle(self, *args, **options):
        email_destino = options['email']

        self.stdout.write(self.style.WARNING('\n' + '='*60))
        self.stdout.write(self.style.WARNING('TESTE DE ENVIO DE EMAIL'))
        self.stdout.write(self.style.WARNING('='*60 + '\n'))

        self.stdout.write(f'Backend configurado: {settings.EMAIL_BACKEND}')
        self.stdout.write(f'Email de destino: {email_destino}\n')

        if 'console' in settings.EMAIL_BACKEND.lower():
            self.stdout.write(self.style.WARNING(
                '⚠️  MODO CONSOLE ATIVADO\n'
                'Os emails serão exibidos AQUI NESTE TERMINAL, não serão enviados!\n'
            ))

        self.stdout.write('Enviando email de teste...\n')

        try:
            from_email = getattr(settings, 'DEFAULT_FROM_EMAIL', 'noreply@avai.com.br')

            send_mail(
                subject='🧪 Email de Teste - Sistema de Votação Avaí FC',
                message='''
Este é um email de teste do Sistema de Votação do Avaí FC.

Se você está vendo esta mensagem:
- No modo CONSOLE: O email aparecerá abaixo neste terminal
- No modo SMTP: O email foi enviado para o endereço real

Atenciosamente,
Sistema de Votação Avaí FC
''',
                from_email=from_email,
                recipient_list=[email_destino],
                fail_silently=False,
            )

            self.stdout.write(self.style.SUCCESS('\n✓ Email enviado com sucesso!'))

            if 'console' in settings.EMAIL_BACKEND.lower():
                self.stdout.write(self.style.WARNING(
                    '\n📧 O email deve ter aparecido ACIMA neste terminal.\n'
                    'Se não apareceu, verifique se há erros.\n'
                ))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'\n✗ Erro ao enviar email: {str(e)}\n'))
            self.stdout.write(self.style.ERROR('Detalhes do erro:'))
            import traceback
            self.stdout.write(traceback.format_exc())

        self.stdout.write('\n' + '='*60 + '\n')

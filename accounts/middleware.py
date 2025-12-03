from django.shortcuts import redirect
from django.urls import reverse


class PasswordChangeMiddleware:
    '''Middleware para forçar mudança de senha no primeiro acesso'''

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Lista de URLs que são permitidas mesmo quando precisa trocar senha
        allowed_urls = [
            reverse('accounts:change_password'),
            reverse('accounts:logout'),
            '/admin/',  # Permitir acesso ao admin Django
        ]

        # Verificar se usuário está autenticado
        if request.user.is_authenticated:
            # Verificar se tem perfil e se precisa trocar senha
            if hasattr(request.user, 'profile'):
                if request.user.profile.must_change_password:
                    # Verificar se não está em uma URL permitida
                    if not any(request.path.startswith(url) for url in allowed_urls):
                        # Redirecionar para página de troca de senha
                        return redirect('accounts:change_password')

        response = self.get_response(request)
        return response

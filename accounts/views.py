from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
from django import forms
import secrets
import string
from business.models import Voting, Vote, Presence
from .models import UserProfile


class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'
    redirect_authenticated_user = True
    
    def get_success_url(self):
        return reverse_lazy('dashboard')
    
    def form_invalid(self, form):
        messages.error(self.request, 'Nome de usuário ou senha incorretos.')
        return super().form_invalid(form)


class RegisterView(CreateView):
    model = User
    template_name = 'accounts/register.html'
    fields = ['username', 'email', 'first_name', 'last_name', 'password']
    success_url = reverse_lazy('accounts:login')
    
    def form_valid(self, form):
        username = form.cleaned_data.get('username')
        email = form.cleaned_data.get('email')
        password1 = self.request.POST.get('password1')
        password2 = self.request.POST.get('password2')

        # Verificar se username já existe
        if User.objects.filter(username=username).exists():
            messages.error(self.request, f'O nome de usuário "{username}" já está em uso. Escolha outro nome.')
            return self.form_invalid(form)

        # Verificar se email já existe (opcional, mas recomendado)
        if email and User.objects.filter(email=email).exists():
            messages.error(self.request, f'O email "{email}" já está cadastrado. Use outro email.')
            return self.form_invalid(form)

        if password1 != password2:
            messages.error(self.request, 'As senhas não coincidem.')
            return self.form_invalid(form)

        user = form.save(commit=False)
        user.set_password(password1)
        user.save()

        messages.success(self.request, 'Cadastro realizado com sucesso! Faça login para continuar.')
        return super().form_valid(form)
    
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        for field in form.fields.values():
            field.required = False
        return form


class CustomLogoutView(LogoutView):
    next_page = 'home'


class CreateConselheiroForm(forms.Form):
    '''Form para cadastro administrativo de conselheiros'''
    username = forms.CharField(
        label='Nome de Usuário',
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-avai-blue bg-gray-700 text-white w-full',
            'placeholder': 'Digite o nome de usuário'
        })
    )
    email = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(attrs={
            'class': 'border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-avai-blue bg-gray-700 text-white w-full',
            'placeholder': 'Digite o email'
        })
    )
    first_name = forms.CharField(
        label='Nome',
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-avai-blue bg-gray-700 text-white w-full',
            'placeholder': 'Digite o nome'
        })
    )
    last_name = forms.CharField(
        label='Sobrenome',
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-avai-blue bg-gray-700 text-white w-full',
            'placeholder': 'Digite o sobrenome'
        })
    )
    is_staff = forms.BooleanField(
        label='Administrador',
        required=False,
        widget=forms.CheckboxInput(attrs={
            'class': 'w-4 h-4 text-avai-blue bg-gray-700 border-gray-300 rounded focus:ring-avai-blue'
        })
    )
    is_superuser = forms.BooleanField(
        label='Superusuário',
        required=False,
        widget=forms.CheckboxInput(attrs={
            'class': 'w-4 h-4 text-avai-blue bg-gray-700 border-gray-300 rounded focus:ring-avai-blue'
        })
    )

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('Este nome de usuário já está em uso.')
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Este email já está cadastrado.')
        return email


class CreateConselheiroView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    '''View administrativa para cadastro de conselheiros'''
    template_name = 'accounts/create_conselheiro.html'

    def test_func(self):
        '''Apenas admins e superusers podem acessar'''
        return self.request.user.is_staff or self.request.user.is_superuser

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CreateConselheiroForm()
        # Recuperar dados do último cadastro da sessão
        if 'last_created_user' in self.request.session:
            context['last_created'] = self.request.session.pop('last_created_user')
        return context

    def post(self, request, *args, **kwargs):
        form = CreateConselheiroForm(request.POST)

        if form.is_valid():
            # Gerar senha temporária aleatória
            alphabet = string.ascii_letters + string.digits
            temporary_password = ''.join(secrets.choice(alphabet) for _ in range(12))

            # Criar usuário
            user = User.objects.create(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
                is_staff=form.cleaned_data['is_staff'],
                is_superuser=form.cleaned_data['is_superuser']
            )
            user.set_password(temporary_password)
            user.save()

            # Configurar perfil para forçar mudança de senha
            profile = user.profile
            profile.must_change_password = True
            profile.temporary_password = temporary_password
            profile.save()

            # Enviar email com credenciais
            email_sent = False
            error_message = None

            try:
                subject = 'Bem-vindo ao Sistema de Votação do Avaí FC'
                message = f'''
Olá {user.get_full_name()},

Seu cadastro no Sistema de Votação do Conselho Deliberativo do Avaí FC foi realizado com sucesso!

Suas credenciais de acesso são:

Nome de Usuário: {user.username}
Senha Temporária: {temporary_password}

IMPORTANTE: Por segurança, você será obrigado a alterar esta senha no primeiro acesso ao sistema.

Para acessar o sistema, visite: {request.build_absolute_uri('/')}

Atenciosamente,
Sistema de Votação Avaí FC
'''
                from_email = getattr(settings, 'DEFAULT_FROM_EMAIL', 'noreply@avai.com.br')

                # Log para debug
                print(f'\n{"="*60}')
                print(f'📧 TENTANDO ENVIAR EMAIL')
                print(f'{"="*60}')
                print(f'Backend: {settings.EMAIL_BACKEND}')
                print(f'De: {from_email}')
                print(f'Para: {user.email}')
                print(f'Assunto: {subject}')

                send_mail(
                    subject=subject,
                    message=message,
                    from_email=from_email,
                    recipient_list=[user.email],
                    fail_silently=False,
                )

                email_sent = True
                print(f'✓ Email enviado/exibido com sucesso!')
                print(f'{"="*60}\n')

            except Exception as e:
                email_sent = False
                error_message = str(e)
                print(f'✗ ERRO ao enviar email: {error_message}')
                print(f'{"="*60}\n')
                import traceback
                traceback.print_exc()

            # Salvar dados na sessão para exibir no template
            request.session['last_created_user'] = {
                'name': user.get_full_name(),
                'username': user.username,
                'email': user.email,
                'password': temporary_password,
                'email_sent': email_sent,
                'error': error_message if not email_sent else None
            }

            return redirect('accounts:create_conselheiro')

        # Se form inválido, reexibir com erros
        context = self.get_context_data()
        context['form'] = form
        return self.render_to_response(context)


class ChangePasswordForm(forms.Form):
    '''Form para mudança obrigatória de senha no primeiro acesso'''
    current_password = forms.CharField(
        label='Senha Atual',
        widget=forms.PasswordInput(attrs={
            'class': 'border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-avai-blue bg-gray-700 text-white w-full',
            'placeholder': 'Digite sua senha atual'
        })
    )
    new_password = forms.CharField(
        label='Nova Senha',
        widget=forms.PasswordInput(attrs={
            'class': 'border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-avai-blue bg-gray-700 text-white w-full',
            'placeholder': 'Digite sua nova senha'
        })
    )
    confirm_password = forms.CharField(
        label='Confirmar Nova Senha',
        widget=forms.PasswordInput(attrs={
            'class': 'border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-avai-blue bg-gray-700 text-white w-full',
            'placeholder': 'Digite novamente sua nova senha'
        })
    )

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)

    def clean_current_password(self):
        current_password = self.cleaned_data.get('current_password')
        if not self.user.check_password(current_password):
            raise forms.ValidationError('Senha atual incorreta.')
        return current_password

    def clean_new_password(self):
        new_password = self.cleaned_data.get('new_password')

        # Validar comprimento mínimo
        if len(new_password) < 8:
            raise forms.ValidationError('A senha deve ter no mínimo 8 caracteres.')

        # Validar presença de números
        if not any(char.isdigit() for char in new_password):
            raise forms.ValidationError('A senha deve conter pelo menos um número.')

        # Validar presença de letras
        if not any(char.isalpha() for char in new_password):
            raise forms.ValidationError('A senha deve conter pelo menos uma letra.')

        return new_password

    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get('new_password')
        confirm_password = cleaned_data.get('confirm_password')

        if new_password and confirm_password:
            if new_password != confirm_password:
                raise forms.ValidationError('As senhas não coincidem.')

        return cleaned_data


class ChangePasswordView(LoginRequiredMixin, TemplateView):
    '''View para mudança obrigatória de senha'''
    template_name = 'accounts/change_password.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = ChangePasswordForm(user=self.request.user)
        context['must_change'] = self.request.user.profile.must_change_password
        return context

    def post(self, request, *args, **kwargs):
        form = ChangePasswordForm(user=request.user, data=request.POST)

        if form.is_valid():
            # Atualizar senha
            new_password = form.cleaned_data['new_password']
            request.user.set_password(new_password)
            request.user.save()

            # Atualizar perfil
            profile = request.user.profile
            profile.must_change_password = False
            profile.temporary_password = None
            profile.save()

            messages.success(request, 'Senha alterada com sucesso!')

            # Re-autenticar usuário com a nova senha
            user = authenticate(username=request.user.username, password=new_password)
            if user is not None:
                login(request, user)

            return redirect('dashboard')

        # Se form inválido, reexibir com erros
        context = self.get_context_data()
        context['form'] = form
        return self.render_to_response(context)


class PendingPasswordChangeView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    '''View para listar usuários com senha temporária (pendentes de mudança)'''
    template_name = 'accounts/pending_password_change.html'

    def test_func(self):
        '''Apenas admins e superusers podem acessar'''
        return self.request.user.is_staff or self.request.user.is_superuser

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Buscar usuários que ainda precisam mudar senha
        pending_users = UserProfile.objects.filter(
            must_change_password=True
        ).select_related('user').order_by('-created_at')

        context['pending_users'] = pending_users
        return context


class DashboardView(LoginRequiredMixin, TemplateView):
    '''View para o dashboard com estatísticas'''

    def get_template_names(self):
        '''Retorna template diferente baseado no tipo de usuário'''
        if self.request.user.is_staff or self.request.user.is_superuser:
            return ['dashboard_admin.html']
        else:
            return ['dashboard_user.html']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        now = timezone.now()

        # Active votings
        active_votings = Voting.objects.filter(
            is_active=True,
            start_date__lte=now,
            end_date__gte=now
        ).select_related('created_by').prefetch_related('options')

        context['active_votings_count'] = active_votings.count()
        context['active_votings'] = active_votings
        context['has_active_votings'] = active_votings.exists()

        # Para usuários comuns, só precisamos das votações ativas
        if not (user.is_staff or user.is_superuser):
            return context

        # Para admins, incluir estatísticas completas
        # User votes count
        context['user_votes_count'] = Vote.objects.filter(user=user).count()

        # User presences count
        context['presences_count'] = Presence.objects.filter(
            user=user,
            present=True
        ).count()

        # Total votings count
        context['total_votings_count'] = Voting.objects.count()

        return context

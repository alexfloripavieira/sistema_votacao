from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView
from django.utils import timezone
from business.models import Voting, Vote, Presence


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

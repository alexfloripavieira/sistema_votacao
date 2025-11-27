from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import ListView, View, DetailView, CreateView, TemplateView
from django.db.models import Q, Count
from django.db import transaction
from django.core.cache import cache
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from django.http import JsonResponse
from .models import Meeting, Presence, Voting, VotingOption, Vote


class MarkPresenceView(LoginRequiredMixin, View):
    '''View para marcar presença do usuário na reunião de hoje'''
    
    def post(self, request, *args, **kwargs):
        today = timezone.now().date()
        
        # Verifica se já marcou presença hoje
        presence, created = Presence.objects.get_or_create(
            user=request.user,
            meeting__meeting_date=today,
            defaults={'present': True}
        )
        
        if created:
            messages.success(request, 'Presença marcada com sucesso!')
        else:
            if presence.present:
                messages.info(request, 'Você já marcou presença hoje.')
            else:
                presence.present = True
                presence.save()
                messages.success(request, 'Presença marcada com sucesso!')
        
        return redirect('business:presence_list')


class PresenceListView(LoginRequiredMixin, ListView):
    '''View para listar todas as presenças'''
    model = Presence
    template_name = 'business/presence_list.html'
    context_object_name = 'presences'
    paginate_by = 20

    def get_queryset(self):
        queryset = Presence.objects.select_related('user', 'meeting').order_by('-meeting__meeting_date', 'user__username')

        # Filtrar por data se fornecida
        date_filter = self.request.GET.get('date')
        if date_filter:
            queryset = queryset.filter(meeting__meeting_date=date_filter)

        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        today = timezone.now().date()
        
        # Verificar se usuário já marcou presença hoje
        context['has_marked_today'] = Presence.objects.filter(
            user=self.request.user,
            meeting__meeting_date=today,
            present=True
        ).exists()
        
        context['today'] = today
        return context


class TodayPresenceListView(LoginRequiredMixin, ListView):
    '''View para listar presenças do dia atual'''
    model = Presence
    template_name = 'business/today_presence_list.html'
    context_object_name = 'presences'
    
    def get_queryset(self):
        today = timezone.now().date()
        return Presence.objects.filter(
            meeting__meeting_date=today,
            present=True
        ).select_related('user').order_by('user__username')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        today = timezone.now().date()
        
        context['has_marked_today'] = Presence.objects.filter(
            user=self.request.user,
            meeting__meeting_date=today,
            present=True
        ).exists()

        context['today'] = today
        context['total_present'] = self.get_queryset().count()
        return context


# ========== VOTING VIEWS ==========

class VotingListView(LoginRequiredMixin, ListView):
    '''View para listar votações ativas'''
    model = Voting
    template_name = 'business/voting_list.html'
    context_object_name = 'votings'
    paginate_by = 10
    
    def get_queryset(self):
        now = timezone.now()
        return Voting.objects.filter(
            is_active=True,
            start_date__lte=now,
            end_date__gte=now
        ).select_related('created_by').prefetch_related('options').order_by('-created_at')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get user's votes for quick reference
        user_votes = Vote.objects.filter(
            user=self.request.user,
            voting__in=context['votings']
        ).values_list('voting_id', flat=True)
        
        context['user_votes'] = list(user_votes)
        return context


class VotingDetailView(LoginRequiredMixin, DetailView):
    '''View para mostrar detalhes de uma votação'''
    model = Voting
    template_name = 'business/voting_detail.html'
    context_object_name = 'voting'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        voting = self.get_object()
        
        # Check if user already voted
        user_vote = Vote.objects.filter(
            voting=voting,
            user=self.request.user
        ).select_related('option').first()
        
        context['user_vote'] = user_vote
        context['has_voted'] = user_vote is not None
        
        # Check if voting is open
        context['is_open'] = voting.is_open()
        
        # Check if user has presence (if required)
        if voting.requires_presence:
            today = timezone.now().date()
            context['has_presence'] = Presence.objects.filter(
                user=self.request.user,
                meeting__meeting_date=today,
                present=True
            ).exists()
        else:
            context['has_presence'] = True
        
        # Get voting options
        context['options'] = voting.options.all().order_by('option_letter')
        
        return context


class CastVoteView(LoginRequiredMixin, View):
    '''View para registrar voto do usuário'''
    
    def post(self, request, pk):
        voting = get_object_or_404(Voting, pk=pk)
        option_id = request.POST.get('option_id')
        
        # Validate voting is open
        if not voting.is_open():
            messages.error(request, 'Esta votação não está mais aberta.')
            return redirect('business:voting_detail', pk=voting.pk)
        
        # Validate option exists
        try:
            option = VotingOption.objects.get(pk=option_id, voting=voting)
        except VotingOption.DoesNotExist:
            messages.error(request, 'Opção inválida.')
            return redirect('business:voting_detail', pk=voting.pk)
        
        # Check if requires presence
        if voting.requires_presence:
            today = timezone.now().date()
            has_presence = Presence.objects.filter(
                user=request.user,
                meeting__meeting_date=today,
                present=True
            ).exists()
            
            if not has_presence:
                messages.error(
                    request, 
                    'Você precisa marcar presença antes de votar.'
                )
                return redirect('business:voting_detail', pk=voting.pk)
        
        # Check if already voted
        if Vote.objects.filter(voting=voting, user=request.user).exists():
            messages.warning(request, 'Você já votou nesta votação.')
            return redirect('business:voting_detail', pk=voting.pk)
        
        # Create vote and update counter
        with transaction.atomic():
            Vote.objects.create(
                voting=voting,
                user=request.user,
                option=option
            )
            option.votes_count += 1
            option.save()
        
        messages.success(request, 'Voto registrado com sucesso!')
        return redirect('dashboard')


class VotingCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    '''View para criar nova votação (apenas staff)'''
    model = Voting
    template_name = 'business/voting_create.html'
    fields = ['title', 'description', 'start_date', 'end_date', 'requires_presence', 'is_active']
    success_url = reverse_lazy('business:voting_list')
    
    def test_func(self):
        return self.request.user.is_staff
    
    def form_valid(self, form):
        form.instance.created_by = self.request.user
        response = super().form_valid(form)
        
        # Create voting options from POST data
        option_letters = self.request.POST.getlist('option_letters[]')
        option_texts = self.request.POST.getlist('option_texts[]')
        
        for letter, text in zip(option_letters, option_texts):
            if letter and text:
                VotingOption.objects.create(
                    voting=self.object,
                    option_letter=letter.upper(),
                    option_text=text
                )
        
        messages.success(self.request, 'Votação criada com sucesso!')
        return response


class VotingResultsView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    '''View para mostrar resultados detalhados de uma votação (apenas staff)'''
    model = Voting
    template_name = 'business/voting_results.html'
    context_object_name = 'voting'

    def test_func(self):
        '''Apenas staff/admin pode ver resultados'''
        return self.request.user.is_staff or self.request.user.is_superuser

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        voting = self.get_object()

        # Get all options with votes
        options_data = []
        for option in voting.options.all().order_by('option_letter'):
            votes = Vote.objects.filter(
                voting=voting,
                option=option
            ).select_related('user').order_by('user__username')

            options_data.append({
                'option': option,
                'votes': votes,
                'percentage': (option.votes_count / voting.total_votes() * 100) if voting.total_votes() > 0 else 0
            })

        context['options_data'] = options_data
        context['total_votes'] = voting.total_votes()
        context['can_view_results'] = True  # Sempre true para staff

        return context


# ========== REPORTS VIEWS ==========

class PresenceReportView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    '''View para relatório de presenças (apenas staff)'''
    model = Presence
    template_name = 'business/presence_report.html'
    context_object_name = 'presences'
    paginate_by = 50
    
    def test_func(self):
        return self.request.user.is_staff
    
    def get_queryset(self):
        queryset = Presence.objects.select_related('user').order_by('-meeting__meeting_date', 'user__username')
        
        # Filter by date range if provided
        start_date = self.request.GET.get('start_date')
        end_date = self.request.GET.get('end_date')
        
        if start_date:
            queryset = queryset.filter(meeting__meeting_date__gte=start_date)
        if end_date:
            queryset = queryset.filter(meeting__meeting_date__lte=end_date)
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Statistics
        queryset = self.get_queryset()
        context['total_presences'] = queryset.filter(present=True).count()
        context['total_absences'] = queryset.filter(present=False).count()
        context['unique_dates'] = queryset.values('meeting__meeting_date').distinct().count()
        
        return context


class VotingReportView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    '''View para relatório detalhado de uma votação (apenas staff)'''
    model = Voting
    template_name = 'business/voting_report.html'
    context_object_name = 'voting'
    
    def test_func(self):
        return self.request.user.is_staff
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        voting = self.get_object()
        
        # Detailed statistics
        options_stats = []
        for option in voting.options.all().order_by('option_letter'):
            votes = Vote.objects.filter(
                voting=voting,
                option=option
            ).select_related('user')
            
            voters_list = [
                {
                    'username': vote.user.username,
                    'full_name': vote.user.get_full_name() or vote.user.username,
                    'voted_at': vote.voted_at
                }
                for vote in votes
            ]
            
            options_stats.append({
                'option': option,
                'votes_count': option.votes_count,
                'voters': voters_list,
                'percentage': (option.votes_count / voting.total_votes() * 100) if voting.total_votes() > 0 else 0
            })
        
        context['options_stats'] = options_stats
        context['total_votes'] = voting.total_votes()
        
        # Eligible voters (if requires presence)
        if voting.requires_presence:
            voting_date = voting.start_date.date()
            context['eligible_voters'] = Presence.objects.filter(
                meeting_date=voting_date,
                present=True
            ).select_related('user').count()
        
        return context


class AdminDashboardView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    '''View para dashboard administrativo (apenas staff)'''
    template_name = 'business/admin_dashboard.html'
    
    def test_func(self):
        return self.request.user.is_staff
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        now = timezone.now()
        today = now.date()
        
        # Try to get statistics from cache
        cache_key = f'admin_dashboard_stats_{today}'
        cached_stats = cache.get(cache_key)
        
        if cached_stats:
            context.update(cached_stats)
        else:
            # Voting statistics
            stats = {
                'total_votings': Voting.objects.count(),
                'active_votings': Voting.objects.filter(
                    is_active=True,
                    start_date__lte=now,
                    end_date__gte=now
                ).count(),
                'upcoming_votings': Voting.objects.filter(
                    is_active=True,
                    start_date__gt=now
                ).count(),
                'completed_votings': Voting.objects.filter(
                    end_date__lt=now
                ).count(),
                'total_votes': Vote.objects.count(),
                'total_users': User.objects.count(),
                'today_presences': Presence.objects.filter(
                    meeting__meeting_date=today,
                    present=True
                ).count(),
                'total_presences': Presence.objects.filter(present=True).count(),
            }
            
            # Cache for 5 minutes
            cache.set(cache_key, stats, 300)
            context.update(stats)
        
        # Recent votings (always fresh)
        context['recent_votings'] = Voting.objects.select_related('created_by').order_by('-created_at')[:5]
        
        # Most active voters (cache separately)
        top_voters_key = 'top_voters'
        top_voters = cache.get(top_voters_key)
        if not top_voters:
            top_voters = list(User.objects.annotate(
                vote_count=Count('votes')
            ).order_by('-vote_count')[:5])
            cache.set(top_voters_key, top_voters, 600)  # 10 minutes
        context['top_voters'] = top_voters
        
        return context


# ========== ADMIN PRESENCE MANAGEMENT VIEWS ==========

class MarkPresenceAdminView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    '''View para admin marcar presença de usuários'''
    model = User
    template_name = 'business/mark_presence_admin.html'
    context_object_name = 'users'
    paginate_by = 50

    def test_func(self):
        return self.request.user.is_staff or self.request.user.is_superuser

    def get_queryset(self):
        queryset = User.objects.filter(is_active=True).order_by('first_name', 'last_name', 'username')

        # Search filter
        search_query = self.request.GET.get('search', '').strip()
        if search_query:
            queryset = queryset.filter(
                Q(username__icontains=search_query) |
                Q(first_name__icontains=search_query) |
                Q(last_name__icontains=search_query) |
                Q(email__icontains=search_query)
            )

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Get active meeting
        active_meeting = Meeting.objects.filter(is_active=True).first()
        context['active_meeting'] = active_meeting

        if active_meeting:
            # Get all presences for active meeting
            meeting_presences = Presence.objects.filter(
                meeting=active_meeting,
                present=True
            ).values_list('user_id', flat=True)

            context['meeting_presences'] = list(meeting_presences)
            context['total_present'] = len(meeting_presences)
        else:
            context['meeting_presences'] = []
            context['total_present'] = 0

        context['search_query'] = self.request.GET.get('search', '')
        context['total_users'] = self.get_queryset().count()

        return context


class TogglePresenceView(LoginRequiredMixin, UserPassesTestMixin, View):
    '''View AJAX para marcar/desmarcar presença de um usuário'''

    def test_func(self):
        return self.request.user.is_staff or self.request.user.is_superuser

    def post(self, request, user_id, *args, **kwargs):
        try:
            user = get_object_or_404(User, id=user_id, is_active=True)

            # Get active meeting
            active_meeting = Meeting.objects.filter(is_active=True).first()
            if not active_meeting:
                return JsonResponse({
                    'success': False,
                    'message': 'Não há reunião ativa. Inicie uma reunião primeiro.'
                }, status=400)

            # Get or create presence for active meeting
            presence, created = Presence.objects.get_or_create(
                user=user,
                meeting=active_meeting,
                defaults={'present': True}
            )

            # Toggle presence
            if not created:
                presence.present = not presence.present
                presence.save()

            return JsonResponse({
                'success': True,
                'present': presence.present,
                'message': f'Presença de {user.get_full_name() or user.username} {"marcada" if presence.present else "desmarcada"} com sucesso!'
            })

        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': f'Erro ao marcar presença: {str(e)}'
            }, status=400)


# ========== MEETING MANAGEMENT VIEWS ==========

class StartMeetingView(LoginRequiredMixin, UserPassesTestMixin, View):
    '''View para iniciar uma nova reunião'''

    def test_func(self):
        return self.request.user.is_staff or self.request.user.is_superuser

    def post(self, request, *args, **kwargs):
        title = request.POST.get('title', '').strip()
        meeting_date = request.POST.get('meeting_date', '').strip()

        if not title or not meeting_date:
            messages.error(request, 'Título e data da reunião são obrigatórios.')
            return redirect('business:admin_dashboard')

        try:
            # Fecha reunião ativa anterior se existir
            Meeting.objects.filter(is_active=True).update(is_active=False, closed_at=timezone.now())

            # Cria nova reunião
            meeting = Meeting.objects.create(
                title=title,
                meeting_date=meeting_date,
                created_by=request.user
            )

            # Cria presenças para todos os usuários (inicialmente False)
            users = User.objects.filter(is_active=True)
            presences = []
            for user in users:
                presences.append(Presence(user=user, meeting=meeting, present=False))
            Presence.objects.bulk_create(presences)

            messages.success(request, f'Reunião "{title}" iniciada com sucesso!')
            return redirect('business:mark_presence_admin')

        except Exception as e:
            messages.error(request, f'Erro ao iniciar reunião: {str(e)}')
            return redirect('business:admin_dashboard')


class CloseMeetingView(LoginRequiredMixin, UserPassesTestMixin, View):
    '''View para encerrar reunião ativa'''

    def test_func(self):
        return self.request.user.is_staff or self.request.user.is_superuser

    def post(self, request, *args, **kwargs):
        try:
            meeting = Meeting.objects.filter(is_active=True).first()
            if not meeting:
                messages.warning(request, 'Não há reunião ativa para encerrar.')
                return redirect('business:admin_dashboard')

            meeting.close_meeting()
            messages.success(request, f'Reunião "{meeting.title}" encerrada com sucesso!')
            return redirect('business:admin_dashboard')

        except Exception as e:
            messages.error(request, f'Erro ao encerrar reunião: {str(e)}')
            return redirect('business:admin_dashboard')


class MeetingListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    '''View para listar reuniões (apenas staff)'''
    model = Meeting
    template_name = 'business/meeting_list.html'
    context_object_name = 'meetings'
    paginate_by = 20

    def test_func(self):
        return self.request.user.is_staff or self.request.user.is_superuser

    def get_queryset(self):
        return Meeting.objects.select_related('created_by').prefetch_related('presences').order_by('-meeting_date', '-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add calculated fields for each meeting
        for meeting in context['meetings']:
            meeting.total_presences_count = meeting.presences.filter(present=True).count()
            meeting.absent_count = meeting.presences.filter(present=False).count()
        return context

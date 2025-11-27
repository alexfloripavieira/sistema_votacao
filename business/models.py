from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Meeting(models.Model):
    title = models.CharField('Título', max_length=200)
    meeting_date = models.DateField('Data da Reunião')
    is_active = models.BooleanField('Ativa', default=True)
    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Criado por',
        related_name='created_meetings'
    )
    created_at = models.DateTimeField('Criado em', auto_now_add=True)
    closed_at = models.DateTimeField('Encerrado em', null=True, blank=True)

    class Meta:
        verbose_name = 'Reunião'
        verbose_name_plural = 'Reuniões'
        ordering = ['-meeting_date', '-created_at']

    def __str__(self):
        status = 'Ativa' if self.is_active else 'Encerrada'
        return f'{self.title} - {self.meeting_date} ({status})'

    def total_presences(self):
        return self.presences.filter(present=True).count()

    def close_meeting(self):
        """Encerra a reunião"""
        self.is_active = False
        self.closed_at = timezone.now()
        self.save()


class Presence(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Usuário',
        related_name='presences'
    )
    meeting = models.ForeignKey(
        Meeting,
        on_delete=models.CASCADE,
        verbose_name='Reunião',
        related_name='presences'
    )
    present = models.BooleanField('Presente', default=False)  # Começa como False
    created_at = models.DateTimeField('Criado em', auto_now_add=True)
    updated_at = models.DateTimeField('Atualizado em', auto_now=True)

    class Meta:
        verbose_name = 'Presença'
        verbose_name_plural = 'Presenças'
        unique_together = ['user', 'meeting']
        ordering = ['meeting__meeting_date', 'user__username']

    def __str__(self):
        return f'{self.user.username} - {self.meeting.title} ({self.meeting.meeting_date})'


class Voting(models.Model):
    title = models.CharField('Título', max_length=200)
    description = models.TextField('Descrição', blank=True)
    start_date = models.DateTimeField('Data de Início')
    end_date = models.DateTimeField('Data de Término')
    requires_presence = models.BooleanField('Requer Presença', default=True)
    is_active = models.BooleanField('Ativa', default=True)
    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Criado por',
        related_name='created_votings'
    )
    created_at = models.DateTimeField('Criado em', auto_now_add=True)
    updated_at = models.DateTimeField('Atualizado em', auto_now=True)
    
    class Meta:
        verbose_name = 'Votação'
        verbose_name_plural = 'Votações'
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title
    
    def is_open(self):
        now = timezone.now()
        return self.is_active and self.start_date <= now <= self.end_date
    
    def total_votes(self):
        return self.votes.count()


class VotingOption(models.Model):
    voting = models.ForeignKey(
        Voting,
        on_delete=models.CASCADE,
        verbose_name='Votação',
        related_name='options'
    )
    option_text = models.CharField('Texto da Opção', max_length=200)
    option_letter = models.CharField('Letra', max_length=1)
    votes_count = models.IntegerField('Contagem de Votos', default=0)
    created_at = models.DateTimeField('Criado em', auto_now_add=True)
    updated_at = models.DateTimeField('Atualizado em', auto_now=True)
    
    class Meta:
        verbose_name = 'Opção de Votação'
        verbose_name_plural = 'Opções de Votação'
        ordering = ['option_letter']
        unique_together = ['voting', 'option_letter']
    
    def __str__(self):
        return f'{self.option_letter}. {self.option_text}'


class Vote(models.Model):
    voting = models.ForeignKey(
        Voting,
        on_delete=models.CASCADE,
        verbose_name='Votação',
        related_name='votes'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Usuário',
        related_name='votes'
    )
    option = models.ForeignKey(
        VotingOption,
        on_delete=models.CASCADE,
        verbose_name='Opção',
        related_name='votes'
    )
    voted_at = models.DateTimeField('Votado em', auto_now_add=True)
    created_at = models.DateTimeField('Criado em', auto_now_add=True)
    updated_at = models.DateTimeField('Atualizado em', auto_now=True)
    
    class Meta:
        verbose_name = 'Voto'
        verbose_name_plural = 'Votos'
        ordering = ['-voted_at']
        unique_together = ['voting', 'user']
    
    def __str__(self):
        return f'{self.user.username} - {self.voting.title}'

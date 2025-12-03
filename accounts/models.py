from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class UserProfile(models.Model):
    '''Perfil do usuário para controle de primeiro acesso'''
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    must_change_password = models.BooleanField(
        'Deve mudar senha',
        default=False,
        help_text='Indica se o usuário deve mudar a senha no próximo login'
    )
    temporary_password = models.CharField(
        'Senha temporária',
        max_length=50,
        blank=True,
        null=True,
        help_text='Senha temporária gerada no cadastro'
    )
    created_at = models.DateTimeField('Criado em', auto_now_add=True)
    updated_at = models.DateTimeField('Atualizado em', auto_now=True)

    class Meta:
        verbose_name = 'Perfil de Usuário'
        verbose_name_plural = 'Perfis de Usuários'

    def __str__(self):
        return f'Perfil de {self.user.username}'


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    '''Cria automaticamente um perfil quando um usuário é criado'''
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    '''Salva o perfil quando o usuário é salvo'''
    if hasattr(instance, 'profile'):
        instance.profile.save()

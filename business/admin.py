from django.contrib import admin
from .models import Meeting, Presence, Voting, VotingOption, Vote


class VotingOptionInline(admin.TabularInline):
    model = VotingOption
    extra = 3
    fields = ['option_letter', 'option_text', 'votes_count']
    readonly_fields = ['votes_count']


@admin.register(Voting)
class VotingAdmin(admin.ModelAdmin):
    list_display = ['title', 'is_active', 'start_date', 'end_date', 'requires_presence', 'created_by', 'total_votes']
    list_filter = ['is_active', 'requires_presence', 'start_date', 'end_date']
    search_fields = ['title', 'description']
    date_hierarchy = 'start_date'
    readonly_fields = ['created_at', 'updated_at']
    inlines = [VotingOptionInline]
    
    fieldsets = (
        ('Informações da Votação', {
            'fields': ('title', 'description', 'created_by')
        }),
        ('Configurações', {
            'fields': ('start_date', 'end_date', 'requires_presence', 'is_active')
        }),
        ('Datas', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)


@admin.register(VotingOption)
class VotingOptionAdmin(admin.ModelAdmin):
    list_display = ['voting', 'option_letter', 'option_text', 'votes_count']
    list_filter = ['voting']
    search_fields = ['option_text', 'voting__title']
    readonly_fields = ['created_at', 'updated_at', 'votes_count']
    
    fieldsets = (
        ('Informações da Opção', {
            'fields': ('voting', 'option_letter', 'option_text', 'votes_count')
        }),
        ('Datas', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display = ['user', 'voting', 'option', 'voted_at']
    list_filter = ['voting', 'voted_at']
    search_fields = ['user__username', 'voting__title']
    date_hierarchy = 'voted_at'
    readonly_fields = ['voted_at', 'created_at', 'updated_at']
    
    fieldsets = (
        ('Informações do Voto', {
            'fields': ('user', 'voting', 'option')
        }),
        ('Datas', {
            'fields': ('voted_at', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


class PresenceInline(admin.TabularInline):
    model = Presence
    extra = 0
    fields = ['user', 'present', 'created_at']
    readonly_fields = ['created_at']
    can_delete = False


@admin.register(Meeting)
class MeetingAdmin(admin.ModelAdmin):
    list_display = ['title', 'meeting_date', 'is_active', 'created_by', 'total_presences', 'created_at']
    list_filter = ['is_active', 'meeting_date']
    search_fields = ['title', 'created_by__username']
    date_hierarchy = 'meeting_date'
    readonly_fields = ['created_at', 'closed_at']
    inlines = [PresenceInline]

    fieldsets = (
        ('Informações da Reunião', {
            'fields': ('title', 'meeting_date', 'is_active', 'created_by')
        }),
        ('Datas', {
            'fields': ('created_at', 'closed_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Presence)
class PresenceAdmin(admin.ModelAdmin):
    list_display = ['user', 'meeting', 'present', 'created_at']
    list_filter = ['meeting', 'present']
    search_fields = ['user__username', 'user__first_name', 'user__last_name', 'meeting__title']
    readonly_fields = ['created_at', 'updated_at']

    fieldsets = (
        ('Informações da Presença', {
            'fields': ('user', 'meeting', 'present')
        }),
        ('Datas', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

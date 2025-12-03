from django.urls import path
from . import views

app_name = 'business'

urlpatterns = [
    # Presence URLs
    path('presence/mark/', views.MarkPresenceView.as_view(), name='mark_presence'),
    path('presence/list/', views.PresenceListView.as_view(), name='presence_list'),
    path('presence/today/', views.TodayPresenceListView.as_view(), name='today_presence'),
    
    # Meeting Management
    path('meeting/start/', views.StartMeetingView.as_view(), name='start_meeting'),
    path('meeting/close/', views.CloseMeetingView.as_view(), name='close_meeting'),
    path('meeting/list/', views.MeetingListView.as_view(), name='meeting_list'),

    # Admin Presence Management
    path('presence/admin/', views.MarkPresenceAdminView.as_view(), name='mark_presence_admin'),
    path('presence/toggle/<int:user_id>/', views.TogglePresenceView.as_view(), name='toggle_presence'),
    
    # Voting URLs
    path('voting/', views.VotingListView.as_view(), name='voting_list'),
    path('voting/<int:pk>/', views.VotingDetailView.as_view(), name='voting_detail'),
    path('voting/<int:pk>/vote/', views.CastVoteView.as_view(), name='cast_vote'),
    path('voting/<int:pk>/results/', views.VotingResultsView.as_view(), name='voting_results'),
    path('voting/<int:pk>/close/', views.CloseVotingView.as_view(), name='close_voting'),
    path('voting/create/', views.VotingCreateView.as_view(), name='voting_create'),
    
    # Reports URLs
    path('reports/presence/', views.PresenceReportView.as_view(), name='presence_report'),
    path('reports/presence/export/excel/', views.ExportPresenceExcelView.as_view(), name='export_presence_excel'),
    path('reports/presence/export/pdf/', views.ExportPresencePDFView.as_view(), name='export_presence_pdf'),
    path('reports/voting/<int:pk>/', views.VotingReportView.as_view(), name='voting_report'),
    path('reports/voting/<int:pk>/export/excel/', views.ExportVotingExcelView.as_view(), name='export_voting_excel'),
    path('reports/voting/<int:pk>/export/pdf/', views.ExportVotingPDFView.as_view(), name='export_voting_pdf'),
    
    # Admin Dashboard
    path('admin-dashboard/', views.AdminDashboardView.as_view(), name='admin_dashboard'),
]

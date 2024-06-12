from django.urls import path
from meuapp.views import TasksView, UsersView, TeamsView, TeamMembersView, TeamInvitationsView, SwaggerView

urlpatterns = [
    path('tasks', TasksView.as_view(), name='tasks-list-create'),
    path('tasks/<int:id>', TasksView.as_view(), name='tasks-detail-update-delete'),
    path('signup', UsersView.as_view(), name='signup'),
    path('signin', UsersView.as_view(), name='signin'),
    path('me', UsersView.as_view(), name='me'),
    path('users/<int:id>', UsersView.as_view(), name='users-update-delete'),
    path('teams', TeamsView.as_view(), name='teams-list-create'),
    path('teams/<int:id>', TeamsView.as_view(), name='teams-detail-update-delete'),
    path('team_members', TeamMembersView.as_view(), name='team-members-list-create'),
    path('team_members/<int:id>', TeamMembersView.as_view(), name='team-members-detail-update-delete'),
    path('team_invitations', TeamInvitationsView.as_view(), name='team-invitations-list-create'),
    path('team_invitations/<int:id>', TeamInvitationsView.as_view(), name='team-invitations-detail-update-delete'),
    path('team_invitations/<int:id>/accept', TeamInvitationsView.as_view(), name='team-invitations-accept'),
    path('swagger', SwaggerView.as_view(), name='swagger-ui'),
    path('swagger.json', SwaggerView.as_view(), name='swagger-json'),
]

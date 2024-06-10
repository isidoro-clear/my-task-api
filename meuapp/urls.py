from django.urls import path
from meuapp.views import TaskView, UserView, TeamView, TeamMemberView

urlpatterns = [
    path('tasks', TaskView.as_view(), name='tasks-list-create'),
    path('tasks/<int:id>', TaskView.as_view(), name='tasks-detail-update-delete'),
    path('signup', UserView.as_view(), name='signup'),
    path('signin', UserView.as_view(), name='signin'),
    path('me', UserView.as_view(), name='me'),
    path('users/<int:id>', UserView.as_view(), name='users-update-delete'),
    path('teams', TeamView.as_view(), name='teams-list-create'),
    path('teams/<int:id>', TeamView.as_view(), name='teams-detail-update-delete'),
    path('team-members', TeamMemberView.as_view(), name='team-members-list-create'),
    path('team-members/<int:id>', TeamMemberView.as_view(), name='team-members-detail-update-delete'),
]

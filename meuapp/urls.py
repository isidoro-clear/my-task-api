from django.urls import path
from meuapp.views import TaskView, UserView

urlpatterns = [
    path('tasks', TaskView.as_view(), name='tasks-list-create'),
    path('tasks/<int:id>', TaskView.as_view(), name='tasks-detail-update-delete'),
    path('signup', UserView.as_view(), name='signup'),
    path('signin', UserView.as_view(), name='signin'),
    path('users/<int:id>', UserView.as_view(), name='users-detail-update-delete'),
]

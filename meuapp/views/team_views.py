from django.http import JsonResponse
from meuapp.views.application_views import ApplicationView
from meuapp.serializers import TeamSerializer
from meuapp.models import Team
from django.utils.decorators import method_decorator
from meuapp.decorators import authenticate_user

class TeamView(ApplicationView):

  @method_decorator(authenticate_user)
  def index(self, request, params):
    teams = Team.objects.filter(user_id=request.current_user_id)
    serialized_teams = TeamSerializer.serialize(teams)
    
    return JsonResponse(serialized_teams, safe=False)
  
  def show(self, request, id, params):
    team = Team.objects.get(id=id)
    serialized_team = TeamSerializer(team)
    return JsonResponse(serialized_team.to_json())
  
  @method_decorator(authenticate_user)
  def create(self, request, params):
    team = Team(**params, **{'user_id': request.current_user_id})
    team.save()
    serialized_team = TeamSerializer(team)
    return JsonResponse(serialized_team.to_json())
  
  def update(self, request, id, params):
    team = Team.objects.get(id=id)
    for key, value in params.items():
      setattr(team, key, value)
    team.save()
    serialized_team = TeamSerializer(team)
    return JsonResponse(serialized_team.to_json())
  
  def destroy(self, request, id, params):
    team = Team.objects.get(id=id)
    team.delete()
    return JsonResponse({'message': 'Team deleted successfully!'})

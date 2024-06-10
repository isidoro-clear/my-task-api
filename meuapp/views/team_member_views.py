from django.http import JsonResponse
from meuapp.views.application_views import ApplicationView
from meuapp.serializers import TeamMemberSerializer
from meuapp.models import TeamMember
from django.utils.decorators import method_decorator
from meuapp.decorators import authenticate_user

class TeamMemberView(ApplicationView):

  @method_decorator(authenticate_user)
  def index(self, request, params):
    teams = TeamMember.objects.filter(user_id=request.current_user_id)
    serialized_teams = TeamMemberSerializer.serialize(teams)
    
    return JsonResponse(serialized_teams, safe=False)
  
  def show(self, request, id, params):
    team = TeamMember.objects.get(id=id)
    serialized_team = TeamMemberSerializer(team)
    return JsonResponse(serialized_team.to_json())
  
  @method_decorator(authenticate_user)
  def create(self, request, params):
    team = TeamMember(**params, **{'user_id': request.current_user_id})
    team.save()
    serialized_team = TeamMemberSerializer(team)
    return JsonResponse(serialized_team.to_json())
  
  def update(self, request, id, params):
    team = TeamMember.objects.get(id=id)
    for key, value in params.items():
      setattr(team, key, value)
    team.save()
    serialized_team = TeamMemberSerializer(team)
    return JsonResponse(serialized_team.to_json())
  
  def destroy(self, request, id, params):
    team = TeamMember.objects.get(id=id)
    team.delete()
    return JsonResponse({'message': 'Team deleted successfully!'})

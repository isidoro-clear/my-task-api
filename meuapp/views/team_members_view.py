from django.http import JsonResponse
from meuapp.views.application_views import ApplicationView
from meuapp.serializers import TeamMemberSerializer
from meuapp.models import TeamMember, Team
from django.utils.decorators import method_decorator
from meuapp.decorators import authenticate_user

class TeamMembersView(ApplicationView):

  @method_decorator(authenticate_user)
  def index(self, request, params):
    teams = Team.objects.filter(user_id=request.current_user_id)
    teamMembers = TeamMember.objects.filter(team__in=teams)
    serialized_teams = TeamMemberSerializer.serialize(teamMembers)
    
    return JsonResponse(serialized_teams, safe=False)
  
  def show(self, request, id, params):
    team = TeamMember.objects.get(id=id)
    serialized_team = TeamMemberSerializer(team)
    return JsonResponse(serialized_team.to_json())
  
  @method_decorator(authenticate_user)
  def create(self, request, params):
    team = Team.objects.filter(user_id=request.current_user_id, id=params['team_id']).first()
    if team is None:
      return JsonResponse({'message': 'You are not allowed to create a team member for this team'}, status=401)
    team_member = TeamMember(**params)
    try:
      team_member.save()
      serialized_team = TeamMemberSerializer(team_member)
      return JsonResponse(serialized_team.to_json(), status=201)
    except ValueError as e:
      return JsonResponse({'errors': str(e)}, status=400)
  
  def update(self, request, id, params):
    team = TeamMember.objects.get(id=id)
    for key, value in params.items():
      setattr(team, key, value)
    try:
      team.save()
      serialized_team = TeamMemberSerializer(team)
      return JsonResponse(serialized_team.to_json())
    except ValueError as e:
      return JsonResponse({'errors': str(e)}, status=400)
  
  def destroy(self, request, id, params):
    team = TeamMember.objects.get(id=id)
    team.delete()
    return JsonResponse({'message': 'Team member deleted successfully!'})

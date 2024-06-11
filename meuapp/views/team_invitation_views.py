from django.http import JsonResponse
from meuapp.views.application_views import ApplicationView
from meuapp.serializers import TeamInvitationSerializer
from meuapp.models import TeamInvitation, Team, TeamMember
from django.utils.decorators import method_decorator
from meuapp.decorators import authenticate_user
from django.views.decorators.csrf import csrf_exempt
import json

class TeamInvitationView(ApplicationView):

  @csrf_exempt
  def dispatch(self, request, *args, **kwargs):
    method = request.method.lower()
    method_map = {
      'get': self.accept if request.path.endswith('/accept') else None,
    }

    params = json.loads(request.body) if method in ['post'] else {}
    
    if method in method_map and method_map[method] is not None:
      return method_map[method](request, **kwargs, params=params)
    return super().dispatch(request, *args, **kwargs)
  
  @method_decorator(authenticate_user)
  def index(self, request, params):
    teams = Team.objects.filter(user_id=request.current_user_id)
    team_invitations = TeamInvitation.objects.filter(team__in=teams)
    serialized_team_invitations = TeamInvitationSerializer.serialize(team_invitations)
    
    return JsonResponse(serialized_team_invitations, safe=False)
  
  def show(self, request, id, params):
    team_invitation = TeamInvitation.objects.get(id=id)
    serialized_team_invitation = TeamInvitationSerializer(team_invitation)
    return JsonResponse(serialized_team_invitation.to_json())
  
  @method_decorator(authenticate_user)
  def create(self, request, params):
    team = Team.objects.get(user_id=request.current_user_id, id=params['team_id'])
    members = TeamMember.objects.filter(team=team)
    if team is None:
      return JsonResponse({'message': 'You are not allowed to create a team invitation for this team'}, status=401)
    if TeamInvitation.objects.filter(email=params['email'], team=team).exists():
      return JsonResponse({'message': 'Team invitation already exists'}, status=401)
    if members.filter(user__email=params['email']).exists():
      return JsonResponse({'message': 'You cannot invite yourself to your own team'}, status=401)
    team_invitation = TeamInvitation(**params)
    team_invitation.save()
    serialized_team_invitation = TeamInvitationSerializer(team_invitation)
    return JsonResponse(serialized_team_invitation.to_json())
  
  def update(self, request, id, params):
    team_invitation = TeamInvitation.objects.get(id=id)
    for key, value in params.items():
      setattr(team_invitation, key, value)
    team_invitation.save()
    serialized_team_invitation = TeamInvitationSerializer(team_invitation)
    return JsonResponse(serialized_team_invitation.to_json())
  
  def destroy(self, request, id, params):
    team_invitation = TeamInvitation.objects.get(id=id)
    team_invitation.delete()
    return JsonResponse({'message': 'Team deleted successfully!'})
    
  def accept(self, request, id, params):
    team_invitation = TeamInvitation.objects.get(id=id)
    team_invitation.status = 'accepted'
    team_invitation.save()
    return JsonResponse({'message': 'Team invitation accepted successfully!'})
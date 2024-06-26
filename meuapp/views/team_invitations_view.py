from django.http import JsonResponse
from meuapp.views.application_views import ApplicationView
from meuapp.serializers import TeamInvitationSerializer
from meuapp.models import TeamInvitation, Team, TeamMember
from django.utils.decorators import method_decorator
from meuapp.decorators import authenticate_user
from django.views.decorators.csrf import csrf_exempt
import json

class TeamInvitationsView(ApplicationView):

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
    team_invitation = TeamInvitation(**params)

    try:
      team_invitation.save()
      serialized_team_invitation = TeamInvitationSerializer(team_invitation)
      return JsonResponse(serialized_team_invitation.to_json(), status=201)
    except ValueError as e:
      return JsonResponse({'errors': str(e)}, status=400)
  
  def update(self, request, id, params):
    team_invitation = TeamInvitation.objects.get(id=id)
    for key, value in params.items():
      setattr(team_invitation, key, value)

    try:
      team_invitation.save()
      serialized_team_invitation = TeamInvitationSerializer(team_invitation)
      return JsonResponse(serialized_team_invitation.to_json())
    except ValueError as e:
      return JsonResponse({'errors': str(e)}, status=400)
  
  def destroy(self, request, id, params):
    team_invitation = TeamInvitation.objects.get(id=id)
    team_invitation.delete()
    return JsonResponse({'message': 'Team deleted successfully!'})
    
  def accept(self, request, id, params):
    team_invitation = TeamInvitation.objects.get(id=id)
    team_invitation.status = 'accepted'
    team_invitation.save()
    return JsonResponse({'message': 'Team invitation accepted successfully!'})
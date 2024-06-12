from django.test import TestCase, Client
from django.urls import reverse
from meuapp.models import TeamInvitation, Team, TeamMember, User

class TeamInvitationsViewTest(TestCase):

  def setUp(self):
    self.client = Client()
    self.user = User.objects.create(
      first_name='John',
      last_name='Doe',
      email='john.doe@example.com',
      password='password'
    )
    self.second_user = {
      'first_name': 'Mary',
      'last_name': 'Doe',
      'email': 'mary.doe@example.com',
      'password': 'password'
    }
    self.team = Team.objects.create(
      name='Team 1',
      description='Team 1 description',
      user_id=self.user.id
    )
    self.team_invitation = TeamInvitation.objects.create(
      team_id=self.team.id,
      email=self.second_user['email']
    )
    self.auth_header = {'HTTP_AUTHORIZATION': f'Bearer {self.user.token()}'}

  def test_index(self):
    response = self.client.get(reverse('team-invitations-list-create'), **self.auth_header)

    self.assertEqual(response.status_code, 200)
    self.assertEqual(response.json()[0]['team_id'], self.team.id)
    self.assertEqual(response.json()[0]['email'], self.second_user['email'])
    self.assertEqual(response.json()[0]['status'], 'pending')

  def test_show(self):
    response = self.client.get(reverse('team-invitations-detail-update-delete', args=[self.team_invitation.id]))

    self.assertEqual(response.status_code, 200)
    self.assertEqual(response.json()['team_id'], self.team.id)
    self.assertEqual(response.json()['email'], self.second_user['email'])
    self.assertEqual(response.json()['status'], 'pending')

  def test_create(self):
    response = self.client.post(reverse('team-invitations-list-create'), {
      'team_id': self.team.id,
      'email': 'jane.doe@example.com',
    }, content_type='application/json', **self.auth_header)

    self.assertEqual(response.status_code, 201)
    self.assertEqual(response.json()['team_id'], self.team.id)
    self.assertEqual(response.json()['email'], 'jane.doe@example.com')
    self.assertEqual(response.json()['status'], 'pending')
  
  def test_accept(self):
    response = self.client.get(reverse('team-invitations-accept', args=[self.team_invitation.id]), {}, content_type='application/json', **self.auth_header)

    accepted_user = User.objects.get(email=self.second_user['email'])
    team_invitation = TeamInvitation.objects.get(id=self.team_invitation.id)
    self.assertEqual(response.status_code, 200)
    self.assertEqual(response.json(), {'message': 'Team invitation accepted successfully!'})
    self.assertEqual(team_invitation.email, self.second_user['email'])
    self.assertEqual(team_invitation.status, 'accepted')
    self.assertEqual(accepted_user.first_name, self.second_user['email'].split('@')[0])
    self.assertEqual(accepted_user.last_name, '')
    self.assertEqual(accepted_user.email, self.second_user['email'])
    self.assertTrue(TeamMember.objects.filter(user_id=accepted_user.id, team_id=self.team.id).exists())
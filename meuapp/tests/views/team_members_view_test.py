from django.test import TestCase, Client
from django.urls import reverse
from meuapp.models import TeamMember, Team, User

class TeamMembersViewTest(TestCase):

  def setUp(self):
    self.client = Client()
    self.user = User.objects.create(
      first_name='John',
      last_name='Doe',
      email='john.doe@example.com',
      password='password'
    )
    self.second_user = User.objects.create(
      first_name='Mary',
      last_name='Doe',
      email='mary.doe@example.com',
      password='password'
    )
    self.team = Team.objects.create(
      name='Team 1',
      description='Team 1 description',
      user_id=self.user.id
    )
    self.team_member = TeamMember.objects.create(
      user_id=self.user.id,
      team_id=self.team.id,
      role='admin'
    )
    self.auth_header = {'HTTP_AUTHORIZATION': f'Bearer {self.user.token()}'}
    self.auth_header_second_user = {'HTTP_AUTHORIZATION': f'Bearer {self.second_user.token()}'}

  def test_index(self):
    response = self.client.get(reverse('team-members-list-create'), **self.auth_header)

    self.assertEqual(response.status_code, 200)
    self.assertEqual(response.json()[0]['user_id'], self.user.id)
    self.assertEqual(response.json()[0]['team_id'], self.team.id)
    self.assertEqual(response.json()[0]['role'], self.team_member.role)

  def test_show(self):
    response = self.client.get(reverse('team-members-detail-update-delete', args=[self.team_member.id]))

    self.assertEqual(response.status_code, 200)
    self.assertEqual(response.json()['user_id'], self.user.id)
    self.assertEqual(response.json()['team_id'], self.team.id)
    self.assertEqual(response.json()['role'], self.team_member.role)
  
  def test_create(self):
    user = User.objects.create(
      first_name='Jane',
      last_name='Doe',
      email= 'jane.doe@example.com',
      password= 'password'
    )
    response = self.client.post(reverse('team-members-list-create'), {
      'user_id': user.id,
      'team_id': self.team.id,
    }, content_type='application/json', **self.auth_header)

    self.assertEqual(response.status_code, 201)
    self.assertEqual(response.json()['user_id'], user.id)
    self.assertEqual(response.json()['team_id'], self.team.id)
    self.assertEqual(response.json()['role'], 'member')

  def test_create_with_invalid_team(self):
    response = self.client.post(reverse('team-members-list-create'), {
      'user_id': self.user.id,
      'team_id': self.team.id,
    }, content_type='application/json', **self.auth_header_second_user)

    self.assertEqual(response.status_code, 401)
    self.assertEqual(response.json(), {'message': 'You are not allowed to create a team member for this team'})

  def test_update(self):
    response = self.client.put(reverse('team-members-detail-update-delete', args=[2]), {
      'role': 'admin',
    }, content_type='application/json', **self.auth_header)

    self.assertEqual(response.status_code, 200)
    self.assertEqual(response.json()['role'], 'admin')
  
  def test_destroy(self):
    response = self.client.delete(reverse('team-members-detail-update-delete', args=[2]), **self.auth_header)

    self.assertEqual(response.status_code, 200)
    self.assertEqual(response.json(), {'message': 'Team member deleted successfully!'})

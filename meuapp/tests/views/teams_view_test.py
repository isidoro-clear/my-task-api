from django.test import TestCase, Client
from django.urls import reverse
from meuapp.models import Team, User

class TeamsViewTest(TestCase):

  def setUp(self):
    self.client = Client()
    self.user = User.objects.create(
      first_name='John',
      last_name='Doe',
      email='john.doe@example.com',
      password='password'
    )
    self.team = Team.objects.create(
      name='Team 1',
      description='Team 1 description',
      user_id=self.user.id
    )
    self.auth_header = {'HTTP_AUTHORIZATION': f'Bearer {self.user.token()}'}

  def test_index(self):
    response = self.client.get(reverse('teams-list-create'), **self.auth_header)
    self.assertEqual(response.status_code, 200)
    self.assertEqual(response.json()[0]['name'], self.team.name)
    self.assertEqual(response.json()[0]['description'], self.team.description)
    self.assertEqual(response.json()[0]['user_id'], self.user.id)

  def test_show(self):
    response = self.client.get(reverse('teams-detail-update-delete', args=[self.team.id]))
    self.assertEqual(response.status_code, 200)
    self.assertEqual(response.json()['name'], self.team.name)
    self.assertEqual(response.json()['description'], self.team.description)
    self.assertEqual(response.json()['user_id'], self.user.id)

  def test_create(self):
    response = self.client.post(reverse('teams-list-create'), {
      'name': 'Team 2',
      'description': 'Team 2 description',
    }, content_type='application/json', **self.auth_header)
    self.assertEqual(response.status_code, 201)
    self.assertEqual(response.json()['name'], 'Team 2')
    self.assertEqual(response.json()['description'], 'Team 2 description')
  
  def test_update(self):
    response = self.client.put(reverse('teams-detail-update-delete', args=[self.team.id]), {
      'name': self.team.name + ' updated',
      'description': self.team.description + ' updated',
    }, content_type='application/json', **self.auth_header)
    self.assertEqual(response.status_code, 200)
    self.assertEqual(response.json()['name'], self.team.name + ' updated')
    self.assertEqual(response.json()['description'], self.team.description + ' updated')
  
  def test_destroy(self):
    response = self.client.delete(reverse('teams-detail-update-delete', args=[self.team.id]), **self.auth_header)
    self.assertEqual(response.status_code, 200)
    self.assertEqual(response.json(), {'message': 'Team deleted successfully!'})

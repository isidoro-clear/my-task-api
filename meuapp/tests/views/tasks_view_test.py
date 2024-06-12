from django.test import TestCase, Client
from django.urls import reverse
from meuapp.models import Task, User

class TasksViewTest(TestCase):

  def setUp(self):
    self.client = Client()
    self.user = User.objects.create(
      first_name='John',
      last_name='Doe',
      email='john.doe@example.com',
      password='password'
    )
    self.task = Task.objects.create(
      title='Task 1',
      description='Task 1 description',
      user_id=self.user.id
    )
    self.auth_header = {'HTTP_AUTHORIZATION': f'Bearer {self.user.token()}'}
  
  def test_index(self):
    response = self.client.get(reverse('tasks-list-create'), **self.auth_header)
    self.assertEqual(response.status_code, 200)
    self.assertEqual(response.json()[0]['title'], 'Task 1')
    self.assertEqual(response.json()[0]['description'], 'Task 1 description')
    self.assertEqual(response.json()[0]['user_id'], self.user.id)
    self.assertFalse(response.json()[0]['completed'])

  def test_show(self):
    response = self.client.get(reverse('tasks-detail-update-delete', args=[self.task.id]))
    self.assertEqual(response.status_code, 200)
    self.assertEqual(response.json()['title'], 'Task 1')
    self.assertEqual(response.json()['description'], 'Task 1 description')
    self.assertEqual(response.json()['user_id'], self.user.id)
    self.assertFalse(response.json()['completed'])

  def test_create(self):
    response = self.client.post(reverse('tasks-list-create'), {
      'title': 'Task 2',
      'description': 'Task 2 description',
    }, content_type='application/json', **self.auth_header)
    self.assertEqual(response.status_code, 201)
    self.assertEqual(response.json()['title'], 'Task 2')
    self.assertEqual(response.json()['description'], 'Task 2 description')

  def test_update(self):
    response = self.client.put(reverse('tasks-detail-update-delete', args=[self.task.id]), {
      'title': 'Task 1 updated',
      'description': 'Task 1 description updated',
    }, content_type='application/json', **self.auth_header)
    self.assertEqual(response.status_code, 200)
    self.assertEqual(response.json()['title'], 'Task 1 updated')
    self.assertEqual(response.json()['description'], 'Task 1 description updated')
  
  def test_destroy(self):
    response = self.client.delete(reverse('tasks-detail-update-delete', args=[self.task.id]), **self.auth_header)
    self.assertEqual(response.status_code, 200)
    self.assertEqual(response.json(), {'message': 'Task deleted successfully!'})

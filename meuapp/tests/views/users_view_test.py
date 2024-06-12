from django.test import TestCase, Client
from django.urls import reverse
from meuapp.models import User

class UsersViewTest(TestCase):

  def setUp(self):
    self.client = Client()
    self.user = User.objects.create(
      first_name='John',
      last_name='Doe',
      email='john.doe@example.com',
      password='password'
    )
    self.auth_header = {'HTTP_AUTHORIZATION': f'Bearer {self.user.token()}'}

  def test_signup(self):
    response = self.client.post(reverse('signup'), {
      'first_name': 'Jane',
      'last_name': 'Doe',
      'email': 'jane.doe@example.com',
      'password': 'password'
    }, content_type='application/json')
    self.assertEqual(response.status_code, 201)
    self.assertEqual(response.json()['first_name'], 'Jane')
    self.assertEqual(response.json()['last_name'], 'Doe')
    self.assertEqual(response.json()['email'], 'jane.doe@example.com')
  
  def test_signin(self):
    response = self.client.post(reverse('signin'), {
      'email': self.user.email,
      'password': self.user.password
    }, content_type='application/json')

    self.assertEqual(response.status_code, 200)
    self.assertEqual(response.json()['first_name'], self.user.first_name)
    self.assertEqual(response.json()['last_name'], self.user.last_name)
    self.assertEqual(response.json()['email'], self.user.email)
    self.assertTrue('Authorization' in response)
    self.assertTrue('Bearer' in response['Authorization'])

  def test_me(self):
    response = self.client.get(reverse('me'), **self.auth_header)
    self.assertEqual(response.status_code, 200)
    self.assertEqual(response.json()['first_name'], self.user.first_name)
    self.assertEqual(response.json()['last_name'], self.user.last_name)
    self.assertEqual(response.json()['email'], self.user.email)
  
  def test_update(self):
    response = self.client.put(reverse('users-update-delete', args=[self.user.id]), {
      'first_name': self.user.first_name + ' updated',
      'last_name': self.user.last_name + ' updated',
    }, content_type='application/json', **self.auth_header)

    self.assertEqual(response.status_code, 200)
    self.assertEqual(response.json()['first_name'], self.user.first_name + ' updated')
    self.assertEqual(response.json()['last_name'], self.user.last_name + ' updated')
  
  def test_destroy(self):
    response = self.client.delete(reverse('users-update-delete', args=[self.user.id]), **self.auth_header)
    self.assertEqual(response.status_code, 200)
    self.assertEqual(response.json(), {'message': 'User deleted successfully!'})

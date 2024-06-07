from django.http import JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
# from meuapp.decorators import authenticate_user
from meuapp.serializers import UserSerializer
from meuapp.models import User
import json

class UserView(View):

  @csrf_exempt
  def dispatch(self, *args, **kwargs):
    method = args[0].method.lower()
    method_map = {
      'post': self.signup if args[0].path == '/signup' else self.signin if args[0].path == '/signin' else None,
      'get': self.show,
      'put': self.update,
      'patch': self.update,
      'delete': self.delete,
    }

    user_params = json.loads(args[0].body) if method in ['post'] else {}
    
    if method in method_map:
      return method_map[method](*args, **kwargs, user_params=user_params)
    else:
      return super().dispatch(*args, **kwargs)

  def signup(self, request, user_params):
    user = User(**user_params)
    user.token = user.token()
    user.save()
    serialized_user = UserSerializer(user)
    return JsonResponse(serialized_user.to_json())
  
  def signin(self, request, user_params):
    user = User.objects.get(email=user_params['email'])
    if user.password == user_params['password']:
      user.token = user.token()
      user.save()
      serialized_user = UserSerializer(user)
      return JsonResponse(serialized_user.to_json())
    else:
      return JsonResponse({'message': 'Invalid credentials'}, status=401)
    
  # @authenticate_user
  def show(self, request, id):
    user = User.objects.get(id=id)
    serialized_user = UserSerializer(user)
    return JsonResponse(serialized_user.to_json())
  
  # @authenticate_user
  def update(self, request, id, user_params):
    user = User.objects.get(id=id)
    for key, value in user_params.items():
      setattr(user, key, value)
    user.save()
    serialized_user = UserSerializer(user)
    return JsonResponse(serialized_user.to_json())
  
  # @authenticate_user
  def delete(self, request, id):
    user = User.objects.get(id=id)
    user.delete()
    return JsonResponse({'message': 'User deleted successfully!'})
    
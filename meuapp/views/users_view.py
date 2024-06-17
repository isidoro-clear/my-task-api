from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from meuapp.decorators import authenticate_user
from django.utils.decorators import method_decorator
from meuapp.views.application_views import ApplicationView
from meuapp.serializers import UserSerializer
from meuapp.models import User
import json

class UsersView(ApplicationView):

  @csrf_exempt
  def dispatch(self, request, *args, **kwargs):
    method = request.method.lower()
    method_map = {
      'post': self.signup if request.path == '/signup' else self.signin if request.path == '/signin' else None,
      'get': self.me,
    }

    params = json.loads(request.body) if method in ['post'] else {}
    
    if method in method_map:
      return method_map[method](request, **kwargs, params=params)
    return super().dispatch(request, *args, **kwargs)

  def signup(self, request, params):
    user = User(**params)
    token = user.token()
    try:
      user.save()
      serialized_user = UserSerializer(user)

      response = JsonResponse(serialized_user.to_json(), status=201)
      response['Authorization'] = f'Bearer {token}'
      return response
    except ValueError as e:
      return JsonResponse({'errors': str(e)}, status=400)
    except Exception as e:
      return JsonResponse({'errors': str(e)}, status=500)
  
  def signin(self, request, params):
    user = User.objects.get(email=params['email'])
    if user.password == params['password']:
      token = user.token()
      user.save()
      serialized_user = UserSerializer(user)
    
      response = JsonResponse(serialized_user.to_json())
      response['Authorization'] = f'Bearer {token}'
      return response
    else:
      return JsonResponse({'message': 'Invalid credentials'}, status=401)
    
  @method_decorator(authenticate_user)
  def me(self, request, params):
    user = User.objects.get(id=request.current_user_id)
    serialized_user = UserSerializer(user)
    return JsonResponse(serialized_user.to_json())
  
  @method_decorator(authenticate_user)
  def update(self, request, id, params):
    if request.current_user_id != id:
      return JsonResponse({'message': 'You are not allowed to update this user'}, status=401)
    user = User.objects.get(id=request.current_user_id)
    for key, value in params.items():
      setattr(user, key, value)
      
    try:
      user.save()
      serialized_user = UserSerializer(user)
      return JsonResponse(serialized_user.to_json())
    except ValueError as e:
      return JsonResponse({'errors': str(e)}, status=400)
  
  
  @method_decorator(authenticate_user)
  def destroy(self, request, id, params):
    if request.current_user_id != id:
      return JsonResponse({'message': 'You are not allowed to delete this user'}, status=401)
    user = User.objects.get(id=request.current_user_id)
    user.delete()
    return JsonResponse({'message': 'User deleted successfully!'})
    
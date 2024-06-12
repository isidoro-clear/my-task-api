from django.views import View
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from meuapp.decorators import authenticate_user
import json

class ApplicationView(View):

  @csrf_exempt
  def dispatch(self, request, *args, **kwargs):
    method = request.method.lower()
    method_map = {
      'get': 'show' if kwargs.get('id') else 'index',
      'post': 'create',
      'put': 'update',
      'patch': 'update',
      'delete': 'destroy',
    }

    params = json.loads(request.body) if method in ['post', 'put', 'patch'] else {}
    
    handler = method_map.get(request.method.lower())
    if handler and hasattr(self, handler):
      return getattr(self, handler)(request, *args, **kwargs, params=params)
    return super().dispatch(request, *args, **kwargs)
  
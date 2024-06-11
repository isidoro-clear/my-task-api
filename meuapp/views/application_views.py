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
      'get': self.show if kwargs.get('id') else self.index,
      'post': self.create,
      'put': self.update,
      'patch': self.update,
      'delete': self.destroy,
    }

    params = json.loads(request.body) if method in ['post', 'put', 'patch'] else {}
    
    if method in method_map:
      return method_map[method](request, *args, **kwargs, params=params)
    return super().dispatch(request, *args, **kwargs)
  
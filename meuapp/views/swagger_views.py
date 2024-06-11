from django.http.response import HttpResponse as HttpResponse
from django.shortcuts import render
from django.http import HttpRequest, JsonResponse
from django.views import View
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
import os
import yaml

class SwaggerView(View):

  @csrf_exempt
  def dispatch(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
    method = request.method.lower()
    method_map = {
      'get': self.json if request.path == '/swagger.json' else self.ui,
    }

    print("METHOD", method_map)
    if method in method_map:
      return method_map[method](request, *args, **kwargs)

  def ui(self, request, *args, **kwargs):
    return render(request, 'swagger_ui.html')
  
  def json(self, request, *args, **kwargs):
    print("BASE_DIR", settings.BASE_DIR)
    swagger_file = os.path.join(settings.BASE_DIR, 'swagger.yaml')
    with open(swagger_file, 'r') as file:
        swagger_data = yaml.safe_load(file)
    return JsonResponse(swagger_data)

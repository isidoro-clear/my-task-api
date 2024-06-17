from django.http import JsonResponse
from meuapp.views.application_views import ApplicationView
from meuapp.serializers import TaskSerializer
from meuapp.models import Task
from django.utils.decorators import method_decorator
from meuapp.decorators import authenticate_user
from django.views.decorators.csrf import csrf_exempt
from meuapp.services import ElasticsearchService

class TasksView(ApplicationView):

  @csrf_exempt
  def dispatch(self, request, *args, **kwargs):
    method = request.method.lower()
    method_map = {
      'get': 'search' if request.path == '/tasks/search' else None,
    }

    params = request.GET if method in ['get'] else {}
    query_params = {
      'match': {
        key: value
      } for key, value in params.items()
    } if params else {'match_all': {}}

    handler = method_map.get(request.method.lower())
    if handler and hasattr(self, handler):
      return getattr(self, handler)(request, *args, **kwargs, params=params, query_params=query_params)
    return super().dispatch(request, *args, **kwargs)

  def search(self, request, params, query_params):
    elasticsearch = ElasticsearchService()
    tasks = elasticsearch.search(index="tasks", query=query_params)
    return JsonResponse(tasks, safe=False)

  @method_decorator(authenticate_user)
  def index(self, request, params):
    tasks = Task.objects.filter(user_id=request.current_user_id)
    serialized_tasks = TaskSerializer.serialize(tasks)
    
    return JsonResponse(serialized_tasks, safe=False)
  
  def show(self, request, id, params):
    task = Task.objects.get(id=id)
    serialized_task = TaskSerializer(task)
    return JsonResponse(serialized_task.to_json())

  @method_decorator(authenticate_user)
  def create(self, request, params):
    task = Task(**params, **{'user_id': request.current_user_id})

    try:
      task.save()
      serialized_task = TaskSerializer(task)
      return JsonResponse(serialized_task.to_json(), status=201)
    except ValueError as e:
      return JsonResponse({'errors': str(e)}, status=400)

  def update(self, request, id, params):
    task = Task.objects.get(id=id)
    for key, value in params.items():
      setattr(task, key, value)
    
    try:
      task.save()
      serialized_task = TaskSerializer(task)
      return JsonResponse(serialized_task.to_json())
    except ValueError as e:
      return JsonResponse({'errors': str(e)}, status=400)
  
  def destroy(self, request, id, params):
    task = Task.objects.get(id=id)
    task.delete()
    return JsonResponse({'message': 'Task deleted successfully!'})
  

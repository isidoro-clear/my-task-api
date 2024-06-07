from django.shortcuts import render
from django.http import JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from meuapp.serializers import TaskSerializer
from meuapp.models import Task
import json

class TaskView(View):

  @csrf_exempt
  def dispatch(self, *args, **kwargs):
    method = args[0].method.lower()
    method_map = {
      'get': self.show if kwargs.get('id') else self.index,
      'post': self.create,
      'put': self.update,
      'patch': self.update,
      'delete': self.delete,
    }

    task_params = json.loads(args[0].body) if method in ['post', 'put', 'patch'] else {}
    
    if method in method_map:
      return method_map[method](*args, **kwargs, task_params=task_params)
    else:
      return super().dispatch(*args, **kwargs)

  def index(self, request):
    tasks = Task.objects.all()
    serialized_tasks = TaskSerializer.serialize(tasks)
    
    return JsonResponse(serialized_tasks, safe=False)
  
  def show(self, request, id):
    task = Task.objects.get(id=id)
    serialized_task = TaskSerializer(task)
    return JsonResponse(serialized_task.to_json())

  def create(self, request, task_params):
    task = Task(**task_params)
    task.save()
    serialized_task = TaskSerializer(task)
    return JsonResponse(serialized_task.to_json())

  def update(self, request, id, task_params):
    task = Task.objects.get(id=id)
    for key, value in task_params.items():
      setattr(task, key, value)
    task.save()
    serialized_task = TaskSerializer(task)
    return JsonResponse(serialized_task.to_json())
  
  def delete(self, request, id):
    task = Task.objects.get(id=id)
    task.delete()
    return JsonResponse({'message': 'Task deleted successfully!'})
  

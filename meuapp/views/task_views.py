from django.http import JsonResponse
from meuapp.views.application_views import ApplicationView
from meuapp.serializers import TaskSerializer
from meuapp.models import Task

class TaskView(ApplicationView):

  def index(self, request, params):
    tasks = Task.objects.all()
    serialized_tasks = TaskSerializer.serialize(tasks)
    
    return JsonResponse(serialized_tasks, safe=False)
  
  def show(self, request, id, params):
    task = Task.objects.get(id=id)
    serialized_task = TaskSerializer(task)
    return JsonResponse(serialized_task.to_json())

  def create(self, request, params):
    task = Task(**params)
    task.save()
    serialized_task = TaskSerializer(task)
    return JsonResponse(serialized_task.to_json())

  def update(self, request, id, params):
    task = Task.objects.get(id=id)
    for key, value in params.items():
      setattr(task, key, value)
    task.save()
    serialized_task = TaskSerializer(task)
    return JsonResponse(serialized_task.to_json())
  
  def destroy(self, request, id, params):
    task = Task.objects.get(id=id)
    task.delete()
    return JsonResponse({'message': 'Task deleted successfully!'})
  

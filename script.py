import os
import sys
import django
from meuapp.services import ElasticsearchService

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'meuprojeto.settings')
django.setup()

from django.apps import apps

def reindex_entities(entity_name):
    es = ElasticsearchService()
    try:
        entity_model = apps.get_model('meuapp', entity_name)
    except AttributeError:
        print(f"Entity {entity_name} not found")
        return
    entities = entity_model.objects.all()
    body = {str(entity.id): entity.to_dict() for entity in entities}
    print(body)
    es.reindex("tasks", body)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python script.py <entity_name>")
        sys.exit(1)
    
    entity_name = sys.argv[1]
    reindex_entities(entity_name)
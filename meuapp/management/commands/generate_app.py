from django.core.management.base import BaseCommand
from django.db import models

class Command(BaseCommand):
    help = 'Generate model, view, and test for an entity'

    TYPE_MAPPING = {
        'email': models.EmailField,
        'string': models.TextField,
        'char': models.CharField,
        'boolean': models.BooleanField,
        'integer': models.IntegerField,
        'references': lambda referenced_model: models.ForeignKey(referenced_model, on_delete=models.CASCADE),
    }

    def create_model_field(self, type_str, *args, **kwargs):
      print("TYPE STR:", type_str)
      if type_str == 'references':
          referenced_model = kwargs.pop('references')
          return models.ForeignKey(referenced_model, on_delete=models.CASCADE, *args, **kwargs)

  
      field_type = self.TYPE_MAPPING.get(type_str)
      if not field_type:
          raise ValueError(f"Unsupported field type: {type_str}")

      return field_type(*args, **kwargs)


    def add_arguments(self, parser):
        print("Adding arguments")
        parser.add_argument('entity_name', type=str, help='The name of the entity')
        parser.add_argument('attributes', type=str, help='Attributes of the entity in the format name:tipo')

    def handle(self, *args, **kwargs):
        entity_name = kwargs['entity_name']
        attributes = kwargs['attributes'].split(',')
        print("Entity name:", entity_name)
        print("Attributes:", attributes)
        # Create model file
        with open(f'meuapp/models/{entity_name.lower()}.py', 'w') as f:
            f.write(f"from django.db import models\n\n"
                    f"class {entity_name}(models.Model):\n")
            for attr in attributes:
                name, type_ = attr.split(':')
                print("Name:", name)
                print("Type:", type_)
                field = self.create_model_field(type_, verbose_name=name.replace('_', ' '), blank=True)
                f.write(f"    {name} = {field}\n")

        # Create views file
        with open(f'meuapp/views/{entity_name.lower()}_view.py', 'w') as f:
            f.write(f"from django.views import View\n"
                    f"class {entity_name}View(View):\n"
                    f"    pass\n")

        # Create tests file
        with open(f'meuapp/tests/test_{entity_name.lower()}.py', 'w') as f:
            f.write(f"from django.test import TestCase\n"
                    f"class Test{entity_name}(TestCase):\n"
                    f"    pass\n")

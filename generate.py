# generate.py
import os
import sys
import django
from django.core.management import execute_from_command_line

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'meuprojeto.settings')
django.setup()

print(sys.argv)
args = sys.argv[1:]
entity_name = args[0]
print("Entity name:", entity_name)
attributes = ','.join(args[1:])
print("Attributes:", attributes)

execute_from_command_line(['manage.py', 'generate_app', entity_name, attributes])

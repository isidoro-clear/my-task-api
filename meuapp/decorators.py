import jwt
from django.http import JsonResponse
from dotenv import dotenv_values
from functools import wraps

def authenticate_user(view_func):
  @wraps(view_func)
  def _wrapped_view(request, *args, **kwargs):
    auth_header = request.headers.get('Authorization', '')

    if not auth_header or not auth_header.startswith('Bearer '):
      return JsonResponse({'error': 'Token not provided or invalid'}, status=401)

    token = auth_header.split(' ')[1]

    try:
        payload = jwt.decode(token, dotenv_values('.env')['JWT_SECRET_KEY'], algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        return JsonResponse({'error': 'Token has expired'}, status=401)
    except jwt.InvalidTokenError:
        return JsonResponse({'error': 'Invalid token'}, status=401)

    request.current_user_id = payload['id']
    return view_func(request, *args, **kwargs)

  return _wrapped_view

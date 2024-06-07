# import jwt
# from django.http import JsonResponse

# def authenticate_user(request):
#   token = request.headers.get('Authorization')
#   if not token:
#     return JsonResponse({'message': 'Token not provided'}, status=401)
  
#   try:
#     payload = jwt
#   except jwt.ExpiredSignatureError:
#     return JsonResponse({'message': 'Token expired'}, status=401)
#   except jwt.InvalidTokenError:
#     return JsonResponse({'message': 'Invalid token'}, status=401)
#   except Exception as e:
#     return JsonResponse({'message': str(e)}, status=401)
  
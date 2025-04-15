from django.http import JsonResponse

from new_tdl_site import settings


class ApiTokenMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith('/api/'):
            api_token = request.headers.get('Authorization')
        # Проверяем наличие заголовка Authorization
            if api_token is None or api_token != f'{settings.API_TOKEN}':
                return JsonResponse({'error': 'Unauthorized'}, status=401)
        return self.get_response(request)
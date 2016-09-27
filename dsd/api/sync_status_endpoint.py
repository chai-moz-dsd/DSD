from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def sync_status(request):
    if request.method == 'GET':
        message = {'message': 'Test message'}

        return JsonResponse(message)


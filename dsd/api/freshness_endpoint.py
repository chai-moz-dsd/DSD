from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def freshness_status(request):
    if request.method == 'GET':
        message = {'message': 'freshness_status'}

        return JsonResponse(message)

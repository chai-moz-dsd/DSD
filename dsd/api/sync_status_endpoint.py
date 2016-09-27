from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView


class SyncStatusList(APIView):

    renderer_classes = (JSONRenderer, )

    def get(self, request):
        message = {'message': 'Test message'}

        return Response(data=message, status=200)

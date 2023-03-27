from .serializers import LogFileSerializer, OperationSerializer, TraceBackSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Operation, TraceBack


class LogFileApi(APIView):
    def post(self, request):
        data = {
            'file': request.FILES['file'],
            'type': request.data['type'],
            'source_name':request.data['source_name']
              }
        serializer = LogFileSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class OperationApi(APIView):
    def get(self, request):
        operations = Operation.objects.all()
        serializer = OperationSerializer(operations, many=True)
        return Response(serializer.data)


class TraceBackApi(APIView):
    def get(self, request):
        tracings = TraceBack.objects.all()
        serializer = TraceBackSerializer(tracings, many=True)
        return Response(serializer.data)
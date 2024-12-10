from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import FaultSerializer
from bookfault.models import bookfaultmodel

@api_view(['GET', 'POST'])
def fault_api(request):
    if request.method == 'POST':
        serializer = FaultSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "data": serializer.data})
        return Response({"status": "error", "errors": serializer.errors})
    if request.method == 'GET':
        faults = bookfaultmodel.objects.all()
        serializer = FaultSerializer(faults, many=True)
        return Response(serializer.data)

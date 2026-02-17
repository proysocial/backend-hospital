from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from medireport.models import RegistroTXT

class ClearRegistroTXT(APIView):

    def delete(self, request):
        total = RegistroTXT.objects.count()
        RegistroTXT.objects.all().delete()

        return Response({
            "mensaje": "Registros eliminados correctamente",
            "registros_eliminados": total
        }, status=status.HTTP_200_OK)

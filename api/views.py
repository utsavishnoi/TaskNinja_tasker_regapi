from rest_framework import viewsets
from .models import Company, User
from .serializers import CompanySerializer, UserSerializer
from rest_framework.decorators import action
from rest_framework.response import Response

class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(detail=False, methods=['get'])
    def filter_companies(self, request):
        work_type = request.query_params.get('work', None)
        if work_type:
            companies = Company.objects.filter(type=work_type)
        else:
            companies = Company.objects.none()  # Return empty queryset if no work type is provided
        serializer = CompanySerializer(companies, many=True)
        return Response(serializer.data)

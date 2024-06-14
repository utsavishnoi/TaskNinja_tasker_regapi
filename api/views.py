from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Tasker
from .serializers import TaskerSerializer

class TaskerViewSet(viewsets.ModelViewSet):
    queryset = Tasker.objects.all()
    serializer_class = TaskerSerializer

    def create(self, request, *args, **kwargs):
        # Printing request data for debugging purposes
        print(request.data)

        # Create serializer with request data
        serializer = self.get_serializer(data=request.data)
        
        # Validate the data
        if not serializer.is_valid():
            # If data is not valid, return errors
            print(serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # If data is valid, save the serializer
        self.perform_create(serializer)
        
        # Retrieve the headers for the created object
        headers = self.get_success_headers(serializer.data)
        
        # Return the serialized data with a 201 status code
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

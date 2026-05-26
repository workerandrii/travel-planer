from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Project
from .serializers import ProjectSerializer

# --- 1. PROJECT ENDPOINTS ---

@api_view(['GET', 'POST'])
def project_list_create(request):
    """
    GET: List all travel projects.
    POST: Create a project (and optionally import a batch of places).
    """
    if request.method == 'GET':
        projects = Project.objects.all().prefetch_related('places')
        serializer = ProjectSerializer(projects, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = ProjectSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

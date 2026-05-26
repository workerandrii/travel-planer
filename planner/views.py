from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Project
from .serializers import ProjectSerializer


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


@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
def project_detail(request, pk):
    """
    GET: Retrieve a single travel project.
    PUT/PATCH: Update travel project info.
    DELETE: Remove project (Blocked if any contained place is marked visited).
    """
    try:
        project = Project.objects.prefetch_related('places').get(pk=pk)
    except Project.DoesNotExist:
        return Response({"detail": "Project not found."}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ProjectSerializer(project)
        return Response(serializer.data)

    elif request.method in ['PUT', 'PATCH']:
        partial = (request.method == 'PATCH')
        serializer = ProjectSerializer(project, data=request.data, partial=partial)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        # A project cannot be deleted if any of its places are already marked as visited
        if project.places.filter(is_visited=True).exists():
            return Response(
                {"detail": "Cannot delete project. One or more places within this project have already been visited."},
                status=status.HTTP_400_BAD_REQUEST
            )
        project.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
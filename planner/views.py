from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Project
from .serializers import ProjectSerializer, PlaceSerializer


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
    

@api_view(['GET', 'POST'])
def project_places_list_create(request, project_id):
    """
    GET: List all places for a specific project.
    POST: Add a single new place to an existing project.
    """
    try:
        project = Project.objects.get(pk=project_id)
    except Project.DoesNotExist:
        return Response({"detail": "Project not found."}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        places = project.places.all()
        serializer = PlaceSerializer(places, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        # Enforce limits (maximum 10 places per project)
        if project.places.count() >= 10:
            return Response({"detail": "Project has reached maximum limit of 10 places."}, status=status.HTTP_400_BAD_REQUEST)

        external_id = request.data.get('external_id')
        if not external_id:
            return Response({"external_id": ["This field is required."]}, status=status.HTTP_400_BAD_REQUEST)

        # Prevent adding the same external place to the same project more than once
        if project.places.filter(external_id=external_id).exists():
            return Response({"detail": "This place has already been added to this project."}, status=status.HTTP_400_BAD_REQUEST)

        serializer = PlaceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(project=project)
            
            # Since an unvisited place was added, the project cannot be marked completed
            project.is_completed = False
            project.save()
            
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
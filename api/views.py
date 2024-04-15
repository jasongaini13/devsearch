from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from  rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from .serializers import projectSerializer  # Corrected serializer name
from projects.models import Project,Review

@api_view(['GET'])
def getRoutes(request):
    routes = [
        {'method': 'GET', 'path': '/api/projects'},
        {'method': 'GET', 'path': '/api/projects/id'},
        {'method': 'POST', 'path': '/api/projects/id/vote'},
        {'method': 'POST', 'path': '/api/users/token'},
        {'method': 'POST', 'path': '/api/users/token/refresh'},
    ]
    return Response(routes)

@api_view(['GET'])
def getProjects(request):
    print('USER:',request.user)
    projects = Project.objects.all()
    serializer = projectSerializer(projects, many=True)  # Corrected serializer name
    return Response(serializer.data)

@api_view(['GET'])
def getProject(request, pk):
    try:
        project = Project.objects.filter(id=pk).first()
    except Project.DoesNotExist:
        return Response({'error': 'Project not found'}, status=404)
    
    serializer = projectSerializer(project)  # Corrected serializer name
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def projectVote(request, pk):
    project = Project.objects.get(id=pk)
    user = request.user.profile
    data = request.data
    review, created = Review.objects.get_or_create(
        owner=user, 
        project=project,
    )
    review.value = data['value']
    review.save()
    
    # The update_vote_count method is called automatically when saving the Review object,
    # so there's no need to call it explicitly here.
    
    serializer = projectSerializer(project, many=False)
    return Response(serializer.data)


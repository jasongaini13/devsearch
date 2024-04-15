from .models import Project, Tag
from django.db.models import Q
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage

def paginateProjects(request,projects,results):

    page = int(request.GET.get('page', 1))  # Convert 'page' to an integer
    paginator = Paginator(projects, results)

    try:
        projects = paginator.page(page)
    except PageNotAnInteger:
        page = 1
        projects = paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages
        projects = paginator.page(page)

    # Calculate left and right indices for pagination
    num_pages = paginator.num_pages
    max_display_pages = 5  # Number of pages to display in pagination
    half_max_display_pages = max_display_pages // 2

    leftIndex = max(1, page - half_max_display_pages)
    rightIndex = min(num_pages + 1, leftIndex + max_display_pages)

    if rightIndex - leftIndex < max_display_pages:
        leftIndex = max(1, rightIndex - max_display_pages)

    custom_range = range(leftIndex, rightIndex)
    return custom_range, projects


def searchProjects(request):

    search_query = request.GET.get('search_query', '')

    projects = Project.objects.all()
    tags = Tag.objects.filter(name__icontains=search_query)
    
    if search_query:

        projects =Project.objects.distinct().filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(owner__name__icontains=search_query) |
            Q(tags__in=tags)
        )

    return projects, search_query
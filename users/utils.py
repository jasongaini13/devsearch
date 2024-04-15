from .models import Profile,Skill
from django.db.models import Q
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage

def paginateProfiles(request,profiles,results):

    page = int(request.GET.get('page', 1))  # Convert 'page' to an integer
    paginator = Paginator(profiles, results)

    try:
        profiles = paginator.page(page)
    except PageNotAnInteger:
        page = 1
        profiles = paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages
        profiles = paginator.page(page)

    # Calculate left and right indices for pagination
    num_pages = paginator.num_pages
    max_display_pages = 5  # Number of pages to display in pagination
    half_max_display_pages = max_display_pages // 2

    leftIndex = max(1, page - half_max_display_pages)
    rightIndex = min(num_pages + 1, leftIndex + max_display_pages)

    if rightIndex - leftIndex < max_display_pages:
        leftIndex = max(1, rightIndex - max_display_pages)

    custom_range = range(leftIndex, rightIndex)
    return custom_range, profiles


def searchProfiles(request):
    search_query = request.GET.get('search_query', '')

    profiles = Profile.objects.all()
    
    if search_query:
        skills = Skill.objects.filter(name__icontains=search_query)
        profiles =Profile.objects.distinct().filter(
            Q(name__icontains=search_query) |
            Q(short_intro__icontains=search_query) |
            Q(skill__in=skills)
        )

    return profiles, search_query
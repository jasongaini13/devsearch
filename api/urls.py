from django.urls import path
from . import views 

 # Assuming your views.py is in the same directory as urls.py
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,)



urlpatterns = [
    path('users/token/', TokenObtainPairView.as_view(),name='token_obtain_pair'),
    path('users/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('', views.getRoutes),
    path('projects/',views.getProjects),
    path('projects/<str:pk>/',views.getProject),
    path('projects/<str:pk>/vote',views.projectVote),
        # Added a comma at the end
]

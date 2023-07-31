from django.urls import path
from .views import ProjectList, AreaAPIView,OptionsView

urlpatterns = [
    path('projects/', ProjectList.as_view(), name='project-create'),
    path('areas/', AreaAPIView.as_view(), name='area-list'),
    path('areas/<int:pk>/', AreaAPIView.as_view(), name='area-detail'),
    path('options/', OptionsView.as_view(), name='Option-detail'),
    # path('projects-filter/', ProjectSearchAPIView.as_view(), name='project-filter'),
]

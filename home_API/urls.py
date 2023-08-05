from django.urls import path
from .views import ProjectList, AreaAPIView, OptionsView, ProjectsView, ProjectView, Images, ImageView, UnitAPIView, \
    InterestedAPIView, FilterAPIView

urlpatterns = [
    path('projects/', ProjectList.as_view(), name='project-create'),
    path('project/', ProjectsView.as_view(), name='project-create'),
    path('unit/<int:project_id>/', UnitAPIView.as_view(), name='unit'),
    path('unit/interested/<int:unit_id>/', InterestedAPIView.as_view(), name='get_interested'),
    path('filter/', FilterAPIView.as_view(), name='get_interested'),
    path('project/<int:pk>', ProjectView.as_view(), name='project-create'),
    path('areas/', AreaAPIView.as_view(), name='area-list'),
    path('areas/<int:pk>/', AreaAPIView.as_view(), name='area-detail'),
    path('options/', OptionsView.as_view(), name='Option-detail'),
    path('images/', Images.as_view()),
    path('image/<int:pk>/', ImageView.as_view())
    # path('projects-filter/', ProjectSearchAPIView.as_view(), name='project-filter'),
]

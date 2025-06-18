from django.urls import path
from .views import ProjectList, AreaAPIView, OptionsView, ProjectsView, ProjectView, Images, ImageView, UnitAPIView, \
    InterestedAPIView, FilterAPIView, FloorMaps, FloorMapView, ProjectDetails, ProjectImages, UnitImages, \
    ProjectsListView, FilterUnits, GovernmentalAreaAPIView, FilterMapUnits, ViewMapProject

urlpatterns = [
    path('projects/', ProjectList.as_view(), name='project-create'),
    path('project/', ProjectView.as_view(), name='project-create'),
    path('project/<int:pk>', ProjectView.as_view(), name='project-create'),
    path('list/project/', ProjectsListView.as_view(), name='project-create'),
    path('unit/<int:project_id>/', UnitAPIView.as_view(), name='unit'),
    path('unit/interested/<int:unit_id>/', InterestedAPIView.as_view(), name='get_interested'),
    path('filter/', FilterUnits.as_view(), name='get_interested'),
    path('map/filter/', FilterMapUnits.as_view(), name='get_interested'),
    path('map/filter/<int:pk>', ViewMapProject.as_view(), name='get_interested'),
    # path('project/<int:pk>', ProjectView.as_view(), name='project-create'),
    path('project/details/<int:id>', ProjectDetails.as_view(), name='project-create'),
    path('areas/', AreaAPIView.as_view(), name='area-list'),
    path('gov_area_in/', GovernmentalAreaAPIView.as_view(), name='gov-area-in'),
    path('areas/<int:pk>/', AreaAPIView.as_view(), name='area-detail'),
    path('options/', OptionsView.as_view(), name='Option-detail'),
    path('images/', Images.as_view()),
    path('image/<int:pk>/', ImageView.as_view()),
    path('images/project/<int:id>/', ProjectImages.as_view(), name='project-create'),
    path('images/unit/<int:id>', UnitImages.as_view(), name='project-create'),
    path('FloorMaps/', FloorMaps.as_view()),
    path('FloorMap/<int:pk>/', FloorMapView.as_view()),
    # path('projects-filter/', ProjectSearchAPIView.as_view(), name='project-filter'),
]

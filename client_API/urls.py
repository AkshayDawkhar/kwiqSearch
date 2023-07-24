from django.urls import path
from .views import ClientAPIView, SearchFilterAPIView, FollowUpAPIView, FeedbackAPIView,FollowUpDate

urlpatterns = [
    path('clients/', ClientAPIView.as_view(), name='client-list'),
    path('searchfilters/', SearchFilterAPIView.as_view(), name='searchfilter-list'),
    path('followups/', FollowUpAPIView.as_view(), name='followup-list'),
    path('feedbacks/', FeedbackAPIView.as_view(), name='feedback-list'),
    path('followups-date/', FollowUpDate.as_view(), name='followup-list'),

]

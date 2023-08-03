from django.urls import path
from .views import ClientAPIView, SearchFilterAPIView, FollowUpsAPIView, FeedbacksAPIView, FollowUpDate, \
    ClientDetailsAPIView, FollowUpAPIView

urlpatterns = [
    path('client/', ClientAPIView.as_view(), name='client-list'),
    path('searchfilters/', SearchFilterAPIView.as_view(), name='searchfilter-list'),
    path('followups/', FollowUpsAPIView.as_view(), name='followup-list'),
    path('followups/<int:id>', FollowUpAPIView.as_view(), name='followup'),
    path('followups-date/', FollowUpDate.as_view(), name='followup-list'),
    path('feedbacks/', FeedbacksAPIView.as_view(), name='feedback-list'),
    path('client/<int:client_id>/', ClientDetailsAPIView.as_view(), name='client-details'),

]

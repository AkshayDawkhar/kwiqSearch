from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Client, SearchFilter, FollowUp, Feedback
from .serializers import ClientSerializer, SearchFilterSerializer, FollowUpSerializer, FeedbackSerializer
from django.shortcuts import get_object_or_404
from datetime import datetime


# View for Client model
class ClientAPIView(APIView):
    def get(self, request):
        clients = Client.objects.all()
        serializer = ClientSerializer(clients, many=True)
        return Response(serializer.data)

    # def post(self, request):
    #     serializer = ClientSerializer(data=request.data)
    #     if serializer.is_valid():
    #         client = serializer.save()
    #         print(client.id)
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def post(self, request):
        client_serializer = ClientSerializer(data=request.data)
        if client_serializer.is_valid():
            client = client_serializer.save()

            # Create SearchFilter instance associated with the newly created client
            search_filter_data = request.data.get('search_filter', {})
            search_filter_data['client'] = client.id
            search_filter_serializer = SearchFilterSerializer(data=search_filter_data)

            if search_filter_serializer.is_valid():
                search_filter_serializer.save()
                response_data = {
                    'client': client_serializer.data,
                    'search_filter': search_filter_serializer.data
                }
                return Response(response_data, status=status.HTTP_201_CREATED)
            else:
                # Delete the newly created client if the SearchFilter creation fails
                client.delete()
                return Response(search_filter_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response(client_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# View for SearchFilter model
class SearchFilterAPIView(APIView):
    def get(self, request):
        filters = SearchFilter.objects.all()
        serializer = SearchFilterSerializer(filters, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = SearchFilterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# View for FollowUp model
class FollowUpAPIView(APIView):
    def get(self, request):
        client_id = request.query_params.get('client_id', None)
        if not client_id:
            return Response("client_id parameter is missing.", status=status.HTTP_400_BAD_REQUEST)

        client = get_object_or_404(Client, id=client_id)
        followups = FollowUp.objects.filter(client=client, done=False)
        serializer = FollowUpSerializer(followups, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = FollowUpSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# View for Feedback model
class FeedbackAPIView(APIView):
    def get(self, request):
        feedbacks = Feedback.objects.all()
        serializer = FeedbackSerializer(feedbacks, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = FeedbackSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            # Get the related follow-up
            follow_up_id = serializer.validated_data['follow_up']
            print(follow_up_id.id)
            follow_up = get_object_or_404(FollowUp, id=follow_up_id.id)

            # Set the follow-up as done
            follow_up.done = True
            follow_up.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FollowUpDate(APIView):
    def get(self, request):
        date_param = request.GET.get('date', None)
        if date_param:
            try:
                # Parse the datetime string to a Python datetime object
                date_param = datetime.strptime(date_param, '%Y-%m-%dT%H:%M:%S.%f')
                # Filter FollowUps based on the provided date
                followups = FollowUp.objects.filter(date_sent__date=date_param.date())
            except ValueError:
                return Response({'error': 'Invalid date format. Use "YYYY-MM-DDTHH:MM:SS.000".'},
                                status=status.HTTP_400_BAD_REQUEST)
        else:
            followups = FollowUp.objects.all()

        serializer = FollowUpSerializer(followups, many=True)
        return Response(serializer.data)

    # def post(self, request):
    #     serializer = FollowUpSerializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ClientDetailsAPIView(APIView):
    def get(self, request, client_id):
        try:
            # Get the client instance based on the provided client_id
            client = Client.objects.get(id=client_id)

            # Serialize the client data
            client_serializer = ClientSerializer(client)

            # Filter followups based on done parameter (optional query parameter)
            done_param = request.GET.get('done', None)
            followups = FollowUp.objects.filter(client=client)
            if done_param:
                followups = followups.filter(done=done_param.lower() == 'true')

            # Filter feedbacks based on response parameter (optional query parameter)
            response_param = request.GET.get('response', None)
            feedbacks = Feedback.objects.filter(follow_up__client=client)
            if response_param:
                feedbacks = feedbacks.filter(response=response_param)

            # Serialize filtered followups and feedbacks
            followup_serializer = FollowUpSerializer(followups, many=True)
            feedback_serializer = FeedbackSerializer(feedbacks, many=True)

            # Combine the serialized data into a single response
            response_data = client_serializer.data
            response_data['followups'] = followup_serializer.data
            response_data['feedback'] = feedback_serializer.data

            return Response(response_data)
        except Client.DoesNotExist:
            return Response({'error': 'Client not found.'}, status=status.HTTP_404_NOT_FOUND)

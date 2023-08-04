from rest_framework import serializers
from .models import Client, SearchFilter, FollowUp, Feedback


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = '__all__'


class SearchFilterSerializer(serializers.ModelSerializer):
    class Meta:
        model = SearchFilter
        fields = '__all__'


class InterestedSearchFilterSerializer(serializers.ModelSerializer):
    fname = serializers.SerializerMethodField()
    lname = serializers.SerializerMethodField()

    class Meta:
        model = SearchFilter
        fields = ['client', 'Area', 'startBudget', 'stopBudget', 'startCarpetArea', 'stopCarpetArea', 'possession',
                  'requirements', 'units', 'fname', 'lname']

    def get_fname(self, obj):
        return obj.client.fname

    def get_lname(self, obj):
        return obj.client.lname


class FollowUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = FollowUp
        fields = '__all__'


class FollowUpDateSerializer(serializers.ModelSerializer):
    fname = serializers.SerializerMethodField()
    lname = serializers.SerializerMethodField()

    class Meta:
        model = FollowUp
        fields = [
            'client',
            'message',
            'actions',
            'date_sent',
            'done',
            'fname',
            'lname'
        ]

    def get_fname(self, obj):
        return obj.client.fname

    def get_lname(self, obj):
        return obj.client.lname


class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = '__all__'

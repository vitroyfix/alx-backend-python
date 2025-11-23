# messaging_app/chats/filters.py
import django_filters
from django.db.models import Q

# Import your Message and Conversation models. Adjust import path to your project.
from .models import Message, Conversation

class MessageFilter(django_filters.FilterSet):
    # Filter messages between two datetimes
    created_at_after = django_filters.IsoDateTimeFilter(field_name='created_at', lookup_expr='gte')
    created_at_before = django_filters.IsoDateTimeFilter(field_name='created_at', lookup_expr='lte')

    # Filter conversation messages that include a specific user id
    # This assumes Conversation has "participants" M2M to User.
    participant = django_filters.NumberFilter(method='filter_by_participant')

    # Optionally filter messages by sender id
    sender = django_filters.NumberFilter(field_name='sender__id', lookup_expr='exact')

    class Meta:
        model = Message
        fields = ['sender', 'created_at_after', 'created_at_before', 'participant']

    def filter_by_participant(self, queryset, name, value):
        """
        Return messages whose conversation has a participant with id=value.
        Adjust the lookup if your Conversation -> participants relation is named differently.
        """
        return queryset.filter(conversation__participants__id=value)

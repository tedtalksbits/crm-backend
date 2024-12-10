# leads/serializers.py
from rest_framework import serializers
from .models import Lead, LeadNote, LeadHistory, Attachment, Comment, Activity

class LeadNoteSerializer(serializers.ModelSerializer):
    created_by_name = serializers.ReadOnlyField(source="created_by.username")

    class Meta:
        model = LeadNote
        fields = ['id', 'text', 'created_by_name', 'tag', 'created_at', 'updated_at']


class LeadHistorySerializer(serializers.ModelSerializer):
    assigned_to_name = serializers.ReadOnlyField(source="assigned_to.username")
    updated_by_name = serializers.ReadOnlyField(source="updated_by.username")

    class Meta:
        model = LeadHistory
        fields = ['id', 'status', 'assigned_to_name', 'updated_by_name', 'updated_at']


class LeadSerializer(serializers.ModelSerializer):
    notes = LeadNoteSerializer(many=True, read_only=True)
    history = LeadHistorySerializer(many=True, read_only=True)
    assigned_to_name = serializers.ReadOnlyField(source="assigned_to.username")
    company_name = serializers.ReadOnlyField(source="company.name")

    class Meta:
        model = Lead
        fields = [
            'id', 'first_name', 'last_name', 'email', 'phone', 'message',
            'status', 'source', 'created_at', 'updated_at', 'assigned_to',
            'assigned_to_name', 'company', 'company_name', 'notes', 'history'
        ]


class AttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attachment
        fields = ['id', 'file', 'created_at']


class CommentSerializer(serializers.ModelSerializer):
    created_by_name = serializers.ReadOnlyField(source="created_by.username")

    class Meta:
        model = Comment
        fields = ['id', 'text', 'created_by_name', 'created_at']


class ActivitySerializer(serializers.ModelSerializer):
    attachments = AttachmentSerializer(many=True, read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    lead_name = serializers.ReadOnlyField(source="lead.first_name")

    class Meta:
        model = Activity
        fields = [
            'id', 'type', 'details', 'due_date', 'is_completed', 'completed_at',
            'created_at', 'updated_at', 'lead', 'lead_name', 'attachments', 'comments'
        ]

class LeadNoteSerializer(serializers.ModelSerializer):
    created_by_name = serializers.ReadOnlyField(source="created_by.username")

    class Meta:
        model = LeadNote
        fields = ['id', 'text', 'created_by_name', 'tag', 'created_at', 'updated_at']

class LeadHistorySerializer(serializers.ModelSerializer):
    assigned_to_name = serializers.ReadOnlyField(source="assigned_to.username")
    updated_by_name = serializers.ReadOnlyField(source="updated_by.username")

    class Meta:
        model = LeadHistory
        fields = ['id', 'status', 'assigned_to_name', 'updated_by_name', 'updated_at']

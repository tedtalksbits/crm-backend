# leads/views.py
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from .models import Lead, Activity, Attachment, Comment, LeadHistory, LeadNote
from .serializers import LeadSerializer, ActivitySerializer, AttachmentSerializer, CommentSerializer, LeadHistorySerializer, LeadNoteSerializer
from backend_project.permissions import IsCompanyUser
class LeadViewSet(ModelViewSet):
    serializer_class = LeadSerializer
    permission_classes = [IsCompanyUser]
    
    def get_queryset(self):
        user = self.request.user
        print(f'User: {user}')
        print(f'User: {user.is_superuser}')
        print(f'User: {user} Is Authenticated: {user.is_authenticated}')
        # Superuser bypass
        if user.is_superuser:
            return Lead.objects.all()
        
        # Filter leads by company
        return Lead.objects.filter(company=user.company)

    def perform_create(self, serializer):
        serializer.save(company=self.request.user.company)
        
class ActivityViewSet(ModelViewSet):
    serializer_class = ActivitySerializer
    permission_classes = [IsAuthenticated, IsCompanyUser]

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return Activity.objects.all()
        return Activity.objects.filter(lead__company=user.company)

    def perform_create(self, serializer):
        serializer.save()

class AttachmentViewSet(ModelViewSet):
    serializer_class = AttachmentSerializer
    permission_classes = [IsAuthenticated, IsCompanyUser]

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return Attachment.objects.all()
        return Attachment.objects.filter(activity__lead__company=user.company)

    def perform_create(self, serializer):
        serializer.save()

class CommentViewSet(ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, IsCompanyUser]

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return Comment.objects.all()
        return Comment.objects.filter(activity__lead__company=user.company)

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
        
class LeadHistoryViewSet(ModelViewSet):
    serializer_class = LeadHistorySerializer
    permission_classes = [IsAuthenticated, IsCompanyUser]

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return LeadHistory.objects.all()
        return LeadHistory.objects.filter(lead__company=user.company)

    def perform_create(self, serializer):
        serializer.save(updated_by=self.request.user)
        
class LeadNoteViewSet(ModelViewSet):
    serializer_class = LeadNoteSerializer
    permission_classes = [IsAuthenticated, IsCompanyUser]

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return LeadNote.objects.all()
        return LeadNote.objects.filter(lead__company=user.company)

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
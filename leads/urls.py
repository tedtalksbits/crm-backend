# leads/urls.py
from rest_framework.routers import DefaultRouter
from .views import LeadViewSet, ActivityViewSet, AttachmentViewSet, CommentViewSet, LeadHistoryViewSet, LeadNoteViewSet

router = DefaultRouter()
router.register(r'leads', LeadViewSet, basename='lead')
router.register(r'activities', ActivityViewSet, basename='activity')
router.register(r'attachments', AttachmentViewSet, basename='attachment')
router.register(r'comments', CommentViewSet, basename='comment')
router.register(r'history', LeadHistoryViewSet, basename='lead_history')
router.register(r'notes', LeadNoteViewSet, basename='lead_note')

urlpatterns = router.urls

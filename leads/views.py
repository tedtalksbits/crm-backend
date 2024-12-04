# leads/views.py
from rest_framework.viewsets import ModelViewSet
from .models import Lead
from .serializers import LeadSerializer

class LeadViewSet(ModelViewSet):
    queryset = Lead.objects.all()
    serializer_class = LeadSerializer

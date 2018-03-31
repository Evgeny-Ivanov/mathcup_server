from rest_framework import generics, filters
from .models import News
from .serializers import NewsSerializer
from common.permissions import IsAdminUserOrReadOnly


class NewsListCreateView(generics.ListCreateAPIView):
    permission_classes = (IsAdminUserOrReadOnly,)
    queryset = News.objects.all()
    serializer_class = NewsSerializer
    filter_backends = (filters.OrderingFilter,)
    ordering_fields = ('date',)


class NewsView(generics.RetrieveAPIView):
    queryset = News.objects.all()
    serializer_class = NewsSerializer

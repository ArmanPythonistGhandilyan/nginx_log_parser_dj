from django_filters.rest_framework import DjangoFilterBackend
from logs.models import NginxLog
from logs.serializers import NginxLogSerializer
from rest_framework import filters, viewsets
from rest_framework.pagination import PageNumberPagination


class NginxLogPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 100


class NginxLogViewSet(viewsets.ModelViewSet):
    queryset = NginxLog.objects.all()
    serializer_class = NginxLogSerializer
    pagination_class = NginxLogPagination
    filter_backends = (filters.OrderingFilter, filters.SearchFilter)
    search_fields = ["ip_address", "uri", "http_method"]
    ordering_fields = ["timestamp", "response_code"]
    ordering = ["-timestamp"]

from django.contrib.postgres.indexes import GinIndex
from django.db import models


class NginxLog(models.Model):
    ip_address = models.GenericIPAddressField()
    timestamp = models.DateTimeField()
    http_method = models.CharField(max_length=10)
    uri = models.TextField()
    response_code = models.IntegerField()
    response_size = models.BigIntegerField()

    def __str__(self):
        return f"{self.ip_address} - {self.http_method} {self.uri}"

    class Meta:
        indexes = [
            models.Index(fields=["ip_address"]),
            models.Index(fields=["timestamp"]),
            models.Index(fields=["response_code"]),
            GinIndex(fields=["uri"]),
        ]

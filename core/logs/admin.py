from django.contrib import admin

from .models import NginxLog


class NginxLogAdmin(admin.ModelAdmin):
    list_display = (
        "ip_address",
        "timestamp",
        "http_method",
        "uri",
        "response_code",
        "response_size",
    )
    list_filter = ("http_method", "response_code", "timestamp")
    search_fields = ("ip_address", "uri", "http_method")
    date_hierarchy = "timestamp"


admin.site.register(NginxLog, NginxLogAdmin)

from django.contrib import admin
from .models import WallapopSearch


@admin.register(WallapopSearch)
class WallapopSearchAdmin(admin.ModelAdmin):
    list_display = (
        "keywords",
        "period",
        "is_active",
        "created_at",
        "updated_at",
    )
    list_filter = ("is_active",)
    search_fields = ("keywords",)
    readonly_fields = ("created_at", "updated_at", "last_id")

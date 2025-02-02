from django.db import models
from django.core.validators import MinValueValidator


class WallapopSearch(models.Model):
    keywords = models.CharField(max_length=255)
    period = models.IntegerField(
        help_text="Check period in minutes", validators=[MinValueValidator(1)]
    )
    is_active = models.BooleanField(default=False)

    last_id = models.CharField(max_length=255, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.keywords} (every {self.period} min)"

    class Meta:
        verbose_name = "Wallapop Search"
        verbose_name_plural = "Wallapop Searches"

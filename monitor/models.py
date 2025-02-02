from django.db import models
from django.core.validators import MinValueValidator
from django_celery_beat.models import PeriodicTask, IntervalSchedule
import json


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

    def schedule_task(self):
        # Delete existing task if any
        PeriodicTask.objects.filter(name=f"wallapop_search_{self.id}").delete()

        if self.is_active:
            # Create or get interval schedule
            schedule, _ = IntervalSchedule.objects.get_or_create(
                every=self.period,
                period=IntervalSchedule.MINUTES,
            )

            # Create periodic task
            PeriodicTask.objects.create(
                interval=schedule,
                name=f"wallapop_search_{self.id}",
                task="monitor.tasks.check_wallapop_search",
                kwargs=json.dumps({"search_id": self.id}),
            )

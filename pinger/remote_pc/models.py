from django.db import models
from django.utils import timezone
from datetime import timedelta

class DS(models.Model):
    OS = (
        ('Windows', 'Windows'),
        ('Linux', 'Linux'),
    )
    name = models.CharField(max_length=50, blank=True, unique=True)
    ip = models.GenericIPAddressField()
    login = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    core = models.PositiveIntegerField()
    ram = models.PositiveIntegerField()
    os = models.CharField(max_length=50,choices=OS)
    last_activity = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f'<{self.pk}> {self.ip} ({self.core}-core {self.ram}GB RAM) {self.os}'

    class Meta:
        verbose_name = 'DS'
        verbose_name_plural = 'DS'

    def ping(self):
        self.last_activity = timezone.now()
        self.save()

    def past(self):
        if self.last_activity:
            delta = timezone.now() - self.last_activity
            return delta
        return ''

    def status(self):
        MAX_LAST_PING = timedelta(minutes=3)
        MAY_BE_WORK_TIME = timedelta(minutes=1.5)
        WORK = {
            'text': 'Работает',
            'color': 'success',
        }
        MAYBE_WORK = {
            'text': 'Работает',
            'color': 'warning',
        }
        NOT_WORK = {
            'text': 'Не работает',
            'color': 'secondary',
        }
        if self.last_activity:
            delta = timezone.now() - self.last_activity
            if delta > MAX_LAST_PING:
                return NOT_WORK
            elif delta > MAY_BE_WORK_TIME:
                return MAYBE_WORK
            else:
                return WORK
        return '-'

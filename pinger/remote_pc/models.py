from django.db import models
from django.utils import timezone
from datetime import timedelta
from django.core.validators import RegexValidator

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
        return f'<{self.name}> {self.ip} {self.os}'

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
        MAX_LAST_PING = timedelta(minutes=4)
        MAY_BE_WORK_TIME = timedelta(minutes=2)
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
        NOT_ACTIVE = {
            'text': '-',
            'color': '-',
        }
        if self.last_activity:
            delta = timezone.now() - self.last_activity
            if delta > MAX_LAST_PING:
                return NOT_WORK
            elif delta > MAY_BE_WORK_TIME:
                return MAYBE_WORK
            else:
                return WORK
        return NOT_ACTIVE

class Settings(models.Model):
    name = models.CharField(
        primary_key=True,
        max_length=50,
        validators=[RegexValidator(regex='^[a-zA-Z_]+$')],
    )
    desc = models.CharField(max_length=255, blank=True)
    value = models.CharField(max_length=255)

    class Meta:
        verbose_name = 'Settings'
        verbose_name_plural = 'Settings'

    def __str__(self):
        return self.name
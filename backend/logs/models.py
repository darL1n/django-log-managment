from django.db import models
from .abstract_models import Log

class LogFile(models.Model):
    ACTIVITY, TRACEBACK = range(2)
    TYPE_CHOICES = [(ACTIVITY, 'Активность'), (TRACEBACK, 'Traceback')]
    type = models.IntegerField(choices=TYPE_CHOICES, default=ACTIVITY)
    file = models.FileField(upload_to='log_files/%Y/%m/%d/')
    created_at = models.DateTimeField(auto_now_add=True)
    source_name = models.CharField(max_length=100)

    def save(self, *args, **kwargs):
        self.file.name = "'{0}', '{1}.log'".format(self.source_name.lower(), self.type)
        super(LogFile, self).save(*args, **kwargs)

    class Meta:
        ordering = ['-id']
        verbose_name = 'Лог-файл'
        verbose_name_plural = 'Лог-файлы'

class Operation(Log):
    pass
    class Meta:
        ordering = ['-id']
        verbose_name = 'Действие'
        verbose_name_plural = 'Действия пользователей'

class TraceBack(Log):
    is_corrected = models.BooleanField(default=False)
    corrected_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        ordering = ['-id']
        verbose_name = 'Трасировку'
        verbose_name_plural = 'Трасировки'
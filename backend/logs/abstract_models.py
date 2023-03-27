from django.db import models

class Log(models.Model):
    NOTSET, DEBUG, INFO, WARNING, ERROR, CRITICAL = range(6)
    LEVEL_CHOICES = [(NOTSET, 'Неназначен'),
                     (DEBUG, 'Дебаг'),
                     (INFO, 'ИНФОРМАТИВНЫЙ'),
                     (WARNING, 'ПРЕДУПРЕЖДЕНИЕ'), 
                     (ERROR, 'ОШИБКА'), 
                     (CRITICAL, 'КРИТИЧЕСКИЙ')]
    
    level = models.IntegerField(choices=LEVEL_CHOICES)
    message = models.TextField(default='')
    created_at = models.DateTimeField()
    module = models.CharField(max_length=50, blank=True, null=True)
    source_name = models.CharField(max_length=100)
    
    class Meta:
        ordering = ['-id']
        verbose_name = 'Лог'
        verbose_name_plural = 'Логи'
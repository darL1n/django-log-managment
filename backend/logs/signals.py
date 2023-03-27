from django.db.models.signals import post_save
from .models import LogFile, Operation, TraceBack
from django.dispatch import receiver
from django.conf import settings
from django.utils import timezone

@receiver(post_save, sender=LogFile)
def create_log(sender, instance, created, **kwargs):
    if created:
        file = instance.file
        file_path = str(settings.BASE_DIR) + file.url
        if instance.type == LogFile.ACTIVITY:
            with open(file_path, 'r') as file:
                lines = file.readlines()
                for line in lines:
                    r = line.split('\t')
                    lvl = r[0][0]
                    final_date = timezone.datetime.strptime(r[1], "%Y-%m-%d %H:%M:%S,%f")
                    module = r[2]
                    msg = r[3]
                    src = instance.source_name
                    Operation.objects.create(level=lvl, created_at=timezone.make_aware(final_date), message=msg, module=module, source_name=src)
                
        if instance.type == LogFile.TRACEBACK:
            with open(file_path, 'r+') as file:
                lines = file.readlines()
                for line in lines:
                    r = line.split('\t')
                    lvl = r[0][0]
                    date = r[1]
                    final_date = timezone.datetime.strptime(date, "%Y-%m-%d %H:%M:%S,%f")
                    msg = r[2]
                    msg = msg.replace('///', '\n')
                    src = instance.source_name
                    TraceBack.objects.create(level=lvl, created_at=timezone.make_aware(final_date), message=msg, source_name=src)

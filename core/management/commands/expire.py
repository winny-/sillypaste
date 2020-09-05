from django.core.management.base import BaseCommand, CommandError
from core.models import Paste, ExpiryLog
from django.utils import timezone
from django.db.models import Sum

class Command(BaseCommand):
    help = 'Delete expired pastes.'

    def handle(self, *args, **options):
        expired = Paste.objects.filter(expiry__lte=timezone.now())
        expiry_log = ExpiryLog.objects.create()
        expiry_log.save()
        if expired:
            expiry_log.count = expired.count()
            expiry_log.expired_ids = ids = [p.id for p in expired]
            expiry_log.reclaimed_space = expired.aggregate(space=Sum('size'))['space']
            print('Found {} expired pastes.  IDs={}'.format(
                len(expired),
                ','.join(map(str, ids)),
            ))
            expired.delete()
            print('Deleted.')
        else:
            print('Found no expired pastes.')
        expiry_log.completed = True
        expiry_log.save()

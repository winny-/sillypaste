from django.core.management.base import BaseCommand, CommandError
from core.models import Paste, ExpiryLog
from django.utils import timezone

class Command(BaseCommand):
    help = 'Delete expired pastes.'

    def handle(self, *args, **options):
        expired = Paste.objects.filter(expiry__lte=timezone.now())
        expiry_log = ExpiryLog.objects.create()
        expiry_log.save()
        if expired:
            info = [(p.id, p.size()) for p in expired]
            expiry_log.count = len(info)
            expiry_log.expired_ids = ids = [pid for (pid, _) in info]
            expiry_log.reclaimed_space = sum(sz for (_, sz) in info)
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

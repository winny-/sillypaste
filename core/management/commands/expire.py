from django.core.management.base import BaseCommand, CommandError
from core.models import Paste, ExpiryLog
from django.utils import timezone
from django.db.models import Sum
import textwrap


class Command(BaseCommand):
    help = 'Delete expired pastes.'

    def handle(self, *args, **options):
        cutoff = timezone.now()
        print(f'Searching for pastes that expire at or before {cutoff}')
        expired = Paste.objects.filter(expiry__lte=cutoff)
        expiry_log = ExpiryLog.objects.create()
        expiry_log.save()
        if expired:
            expiry_log.count = expired.count()
            expiry_log.expired_ids = ids = [p.id for p in expired]
            expiry_log.reclaimed_space = expired.aggregate(space=Sum('size'))['space']
            print(f'Found {len(expired)} pastes:')
            sp_sep_ids = ' '.join(map(str, ids))
            block = textwrap.indent(textwrap.fill(sp_sep_ids), ' ' * 4)
            print(block)
            expired.delete()
            print('Deleted.')
        else:
            print('Found no expired pastes.')
        expiry_log.completed = True
        expiry_log.save()

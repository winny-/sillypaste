from django.core.management.base import BaseCommand, CommandError
from core.models import Paste, ExpiryLog
from django.utils import timezone
from django.db.models import Sum
from datetime import timedelta
from lazysignup.models import LazyUser
import textwrap


class Command(BaseCommand):
    help = 'Delete expired pastes.'

    def handle(self, *args, **options):
        expiry_cutoff = now = timezone.now()
        print(f'Searching for pastes that expire at or before {expiry_cutoff}')
        expired = Paste.objects.filter(expiry__lte=expiry_cutoff)
        expiry_log = ExpiryLog.objects.create()
        expiry_log.save()
        if expired:
            expiry_log.count = expired.count()
            expiry_log.expired_ids = ids = [p.id for p in expired]
            expiry_log.reclaimed_space = expired.aggregate(space=Sum('size'))['space']
            print(f'Found {expired.count()} pastes:')
            sp_sep_ids = ' '.join(map(str, ids))
            block = textwrap.indent(textwrap.fill(sp_sep_ids), ' ' * 4)
            print(block)
            expired.delete()
            print('Deleted the pastes.')
        else:
            print('Found no expired pastes.')

        user_cutoff = now - timedelta(days=30*6)
        print(f'Searching for old lazy users from before {user_cutoff}')
        old_users = LazyUser.objects.filter(user__last_login__lt=user_cutoff)
        if old_users:
           print(f'Found {old_users.count()} lazy users.')
           expiry_log.user_count = old_users.count()
           old_users.delete()
           print('Deleted the users.')
        else:
            print('Found no old lazy users.')

        expiry_log.completed = True
        expiry_log.save()

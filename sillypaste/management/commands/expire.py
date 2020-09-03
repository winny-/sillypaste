from django.core.management.base import BaseCommand, CommandError
from core.models import Paste
from django.utils import timezone

class Command(BaseCommand):
    help = 'Delete expired pastes.'

    def handle(self, *args, **options):
        expired = Paste.objects.filter(expiry__lte=timezone.now())
        if expired:
            print('Found {} expired pastes.  IDs={}'.format(
                len(expired),
                ','.join(str(p.id) for p in expired),
            ))
            expired.delete()
            print('Deleted.')
        else:
            print('Found no expired pastes.')

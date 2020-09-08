from django.core.management.base import BaseCommand, CommandError
from core.models import Language
from pygments import lexers


class Command(BaseCommand):
    help = 'Populate the Language model from pygments lexer data.'

    def handle(self, *args, **options):
        names = {lex[0] for lex in lexers.get_all_lexers()}
        unknown = Language.objects.exclude(name__in=names).order_by('pk')
        if unknown.exists():
            print('!!! Unknown lexers in database.')
            for u in unknown:
                print(f'{u.pk:<4} {u.name}')
            if input('Continue and DELETE y/n? ') != 'y':
                return
            unknown.delete()
        print('Updating database...', end='', flush=True)
        for n in names:
            print(' ', n, sep='', end='', flush=True)
            lang = Language.objects.get_or_create(name=n)
        print()
        print('DONE')

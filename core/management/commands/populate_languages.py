from django.core.management.base import BaseCommand, CommandError
from core.models import Language
from pygments import lexers
import sys


class Command(BaseCommand):
    help = 'Populate the Language model from pygments lexer data.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--remove-unknown',
            action='store_true',
            help='Remove unknown lexers from the database',
        )

    def handle(self, *args, **options):
        names = {lex[0] for lex in lexers.get_all_lexers()} | Language.RENDERABLE_LANGUAGES
        unknown = Language.objects.exclude(name__in=names).order_by('pk')
        if unknown.exists():
            print('!!! Unknown lexers in database.')
            for u in unknown:
                print(' ' * 4, f'id={u.pk:<4} name="{u.name}"', sep='')
            if not options['remove_unknown']:
                if not sys.stdin.isatty():
                    print('!!! stdin is not a tty.  Add --remove-unknown to invocation or run interactively.  Aborting.')
                    return
                if input('Continue and DELETE y/n? ') != 'y':
                    return
            unknown.delete()
            print('Deleted.', end='\n\n')
        print('Updating database...')
        unprinted_names = []
        width = 0
        for n in names:
            unprinted_names.append(n)
            width += len(n) + 1
            lang = Language.objects.get_or_create(name=n)
            if width > 64:
                print(' ' * 4, ' '.join(unprinted_names), sep='')
                width = 0
                unprinted_names = []
        if unprinted_names:
            print(' ' * 4, ' '.join(unprinted_names), sep='')
        print('DONE')

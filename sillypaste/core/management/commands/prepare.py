from django.core.management.base import BaseCommand
import sys
import subprocess


class Command(BaseCommand):
    help = 'Prepare database and static files for webhosting..'

    def handle(self, *args, **options):
        base = sys.argv[: sys.argv.index('prepare')]

        def run(subcommand):
            subprocess.run(base + subcommand.split(' '))

        run('collectstatic --noinput')
        run('migrate')
        run('populate_languages --remove-unknown')
        run('expire')

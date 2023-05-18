from django.core.management.base import BaseCommand
import sys
import subprocess
import os


class Command(BaseCommand):
    help = 'Serve the website.'

    def handle(self, *args, **options):
        base = sys.argv[: sys.argv.index('serve')]
        subprocess.run(base + ['prepare'])
        os.execlp(
            "gunicorn", "gunicorn", "-b", "0.0.0.0:8000", "sillypaste.cfg.wsgi"
        )

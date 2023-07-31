from django.core.management.base import BaseCommand
import sys
import subprocess
import os


class Command(BaseCommand):
    help = 'Serve the website.'

    def handle(self, *args, **options):
        base = sys.argv[: sys.argv.index('serve')]
        subprocess.run(base + ['prepare'])

        # See flag args here:
        #   https://docs.gunicorn.org/en/stable/settings.html
        os.execlp(
            "gunicorn",
            "gunicorn",
            # Bind to an address:port.
            "-b",
            "0.0.0.0:8000",
            # Log traffic to stdout.
            "--access-logfile",
            "-",
            # Via https://stackoverflow.com/a/51723071/2720026
            "--capture-output",
            "--enable-stdio-inheritance",
            "sillypaste.cfg.wsgi",
        )

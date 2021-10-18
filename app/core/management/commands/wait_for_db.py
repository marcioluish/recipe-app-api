import time

from psycopg2 import OperationalError as Psycopyg2OpError

from django.db import connections
from django.db.utils import OperationalError
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """Django command to pause execution until dabatase is available"""

    def handle(self, *args, **options):
        self.stdout.write('Waiting for database...')
        db_conn = None
        while not db_conn:
            try:
                # connections['default'] returns the connection status to
                # (cont)the default database.
                # Default database is set in settings.py file
                db_conn = connections['default']
            except (OperationalError, Psycopyg2OpError):
                self.stdout.write('Database unavailable, waiting 1 second...')
                time.sleep(1)

        self.stdout.write(self.style.SUCCESS('Database available!'))

"""
Becouse of this directory structure django will
automaticaly detect this as a management command that
will be run using manage.py
Django command to wait for the database to be available.
"""
import time
from psycopg2 import OperationalError as Psycopg2OpError
from django.db.utils import OperationalError
from django.core.management.base import BaseCommand

# BaseCommand has a check method that allows us
# to check the status of the database


class Command(BaseCommand):
    """Django command to wait for database."""
    # Check the database -> Wait a few seconds -> then check again
    # We dont want a thousands of requests to check the database..
    def handle(self, *args, **options):
        self.stdout.write('Waiting for database...')
        db_up = False
        while db_up is False:
            try:
                self.check(databases=['default'])
                db_up = True
            except (Psycopg2OpError, OperationalError):
                self.stdout.write('Database unavailable, waitting 1 second...')
                # Python is going to stop here for one second
                time.sleep(1)

        self.stdout.write(self.style.SUCCESS('Database available!'))

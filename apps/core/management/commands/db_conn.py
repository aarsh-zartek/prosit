import time
from typing import Any, Optional

from django.core.management.base import BaseCommand
from django.db import DEFAULT_DB_ALIAS, connection
from django.db.utils import OperationalError
from django.utils.translation import ngettext

# Create your commands here.


class Command(BaseCommand):
    """Django management command that waits for database to be available"""

    help = "Check database connection"

    def add_arguments(self, parser):
        parser.add_argument(
            "--seconds",
            "-s",
            nargs="?",
            type=int,
            help="Number of seconds to wait before retrying",
            default=3,
        )
        parser.add_argument(
            "--retries",
            "-r",
            nargs="?",
            type=int,
            help="Number of retries before exiting",
            default=5,
        )
        parser.add_argument(
            "--database",
            type=str,
            help=(
                "Ensures connections to a specific database. "
                'Defaults to the "default" database.'
            ),
            default=DEFAULT_DB_ALIAS,
        )

    def handle(self, *args: Any, **options: Any) -> Optional[str]:
        """Handle the command"""


        self.stdout.write(self.style.HTTP_INFO("Waiting for database..."))

        wait, retries = options["seconds"], options["retries"]
        current_retries = 0
        while current_retries < retries:
            current_retries += 1
            try:
                connection.ensure_connection()
                self.stdout.write(self.style.SUCCESS("Database connected"))
                break
            except OperationalError:
                plural_time = ngettext("second", "seconds", wait)
                self.stdout.write(
                    self.style.WARNING(
                        f"Database unavailable, retrying after {wait} {plural_time}!"
                    )
                )
                time.sleep(wait)

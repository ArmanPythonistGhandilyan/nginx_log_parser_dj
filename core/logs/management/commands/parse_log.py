import os
import re
from datetime import datetime
from typing import Type

from django.core.management.base import BaseCommand
from logs.models import NginxLog

from ._log_pattern import LOG_PATTERN
from ._resources import AWSS3, GoogleDrive, RegularAPI


class Command(BaseCommand):
    """
    A Django management command to parse and save nginx log files from a remote URL.

    The command currently supports resources from Google Drive.
    """

    help = "Parse and save nginx log file from a remote URL"

    def add_arguments(self, parser):
        parser.add_argument("url", type=str)

    def handle(self, **kwargs):
        url = kwargs["url"]
        self.stdout.write(self.style.NOTICE("Determining resource type..."))
        resource = self.get_resource(url=url)
        if not resource:
            self.stderr.write(
                self.style.ERROR("Unsupported URL format or resource type.")
            )
            return

        self.stdout.write(self.style.NOTICE("Downloading log file..."))
        try:
            local_file_path = resource.download("nginx.log")
            self.parse_and_save_log(local_file_path)
            self.stdout.write(self.style.SUCCESS("Log file processed and cleaned up."))
        except RuntimeError as e:
            self.stderr.write(self.style.ERROR(f"Error: {e}"))
        finally:
            if os.path.exists(local_file_path):
                os.remove(local_file_path)

    def parse_and_save_log(self, file_path, batch_size=1000):
        self.stdout.write(self.style.NOTICE("Parsing... "))
        log_entries = []  # Buffer to store logs before bulk insertion

        with open(file_path, "r") as file:
            for line in file:
                match = re.match(LOG_PATTERN, line)
                if match:
                    log_data = match.groupdict()
                    timestamp = datetime.strptime(
                        log_data["time"], "%d/%b/%Y:%H:%M:%S %z"
                    )

                    log_entry = NginxLog(
                        ip_address=log_data["remote_ip"],
                        timestamp=timestamp,
                        http_method=log_data["method"],
                        uri=log_data["uri"],
                        response_code=int(log_data["response"]),
                        response_size=int(log_data["bytes"]),
                    )
                    log_entries.append(log_entry)

                    # Once the batch is filled, bulk insert and reset the list
                    if len(log_entries) >= batch_size:
                        NginxLog.objects.bulk_create(log_entries)
                        log_entries = []

            # Final bulk insert for remaining logs
            if log_entries:
                NginxLog.objects.bulk_create(log_entries)

        self.stdout.write(
            self.style.SUCCESS("Successfully parsed and saved in the database")
        )

    def get_resource(self, url: str):
        if "google.com" in url:
            return GoogleDrive(url=url, command=self)
        elif "s3.amazonaws.com" in url:
            return AWSS3(url=url, command=self)
        else:
            return RegularAPI(url=url, command=self)

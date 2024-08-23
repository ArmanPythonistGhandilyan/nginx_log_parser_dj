import re
from abc import ABC, abstractmethod

import requests
from django.core.management.base import BaseCommand
from tqdm import tqdm


class BaseResource(ABC):
    @abstractmethod
    def download(self, destination):
        pass

    def save_response_content(self, response, destination):
        CHUNK_SIZE = 32768
        total_size = int(response.headers.get("content-length", 0))
        with open(destination, "wb") as f:
            with tqdm(
                total=total_size, unit="B", unit_scale=True, unit_divisor=1024
            ) as bar:
                for chunk in response.iter_content(CHUNK_SIZE):
                    if chunk:
                        f.write(chunk)
                        bar.update(len(chunk))


class GoogleDrive(BaseResource):
    def __init__(self, url, command: BaseCommand) -> None:
        self.url = url
        self.command = command

    def download(self, destination):
        file_id = self.extract_file_id(self.url)
        URL = "https://docs.google.com/uc?export=download"

        response = self._get_response(URL, params={"id": file_id})

        token = self.get_confirm_token(response)
        if token:
            response = self._get_response(
                URL,
                params={"id": file_id, "confirm": token},
            )

        self.save_response_content(response, destination)
        self.command.stdout.write(
            self.command.style.SUCCESS("Downloaded successfully"),
        )
        return destination

    def _get_response(self, url, params=None):
        session = requests.Session()
        try:
            response = session.get(url, params=params, stream=True)
            response.raise_for_status()
            return response
        except requests.RequestException as e:
            self.command.stderr.write(
                self.command.style.ERROR(f"Error downloading file: {e}")
            )
            raise RuntimeError(f"Error downloading file: {e}")
        except Exception as e:
            self.command.stderr.write(
                self.command.style.ERROR(f"An unexpected error occurred: {e}")
            )
            raise RuntimeError(f"An unexpected error occurred: {e}")

    @staticmethod
    def extract_file_id(url):
        match = re.search(r"/d/([^\s/]+)", url)
        if match:
            return match.group(1)
        raise ValueError("Invalid Google Drive URL")

    @staticmethod
    def get_confirm_token(response):
        for key, value in response.cookies.items():
            if key.startswith("download_warning"):
                return value
        return None


class RegularAPI(BaseResource):

    def download(self, destination):
        raise NotImplementedError("RegularAPI download method not implemented")


class AWSS3(BaseResource):

    def download(self, destination):
        raise NotImplementedError("AWSS3 download method not implemented")

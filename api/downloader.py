import logging
import zipfile
import requests
import os

from requests.exceptions import ConnectionError, HTTPError, Timeout
from datetime import datetime


log = logging.getLogger()


class ResourceDownloader:
    BOOTSTRAP_URL = 'https://github.com/twbs/bootstrap/releases/download/v4.0.0/bootstrap-4.0.0-dist.zip'

    def __init__(
        self,
        target_file_path: str = '',
        project_type: str = 'native'
    ) -> None:
        self.target_file_path, self.project_type = target_file_path, project_type
        self.file_content = None
        self.new_file_name = None

    def get_bootstrap(self):
        self.send_request()
        self.write_file()
        self.unpack_relevant_files()
        self.cleanup()

    def send_request(self) -> None:
        try:
            log.info(f'Requesting {self.BOOTSTRAP_URL}.')
            self.file_content = requests.get(self.BOOTSTRAP_URL).content

        except (
            ConnectionError,
            HTTPError,
            Timeout
        ) as e:
            log.error(f'Request failed.\n{e}', exc_info=True)

    def write_file(self) -> None:
        try:
            log.info('Downloading bootstrap.')
            self.new_file_name = f"bs_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.zip"

            with open(self.new_file_name, 'wb') as f:
                f.write(self.file_content)

        except (
            IOError,
            FileNotFoundError,
            FileExistsError
        ) as e:
            log.error(f'Unable to write file.\n{e}', exc_info=True)

    def unpack_relevant_files(self) -> None:
        try:
            log.info(f'Unpacking {self.new_file_name}.')

            with (zipfile.ZipFile(self.new_file_name, 'r') as z):
                dest_folder = 'assets' if self.project_type == 'native' else 'static'

                z.extract('css/bootstrap.min.css', os.path.join(self.target_file_path, dest_folder))
                z.extract('js/bootstrap.min.js', os.path.join(self.target_file_path, dest_folder))

        except (FileNotFoundError, FileExistsError) as e:
            log.error('Something went wrong...')

    def cleanup(self):
        try:
            log.info(f'Cleaning up- deleting {self.new_file_name}')
            os.remove(self.new_file_name)

        except (FileNotFoundError, FileExistsError, NotADirectoryError) as e:
            log.info(f'Unable to delete file.\n{e}', exc_info=True)

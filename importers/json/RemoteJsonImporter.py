import os
import requests
from typing import TYPE_CHECKING
from importers.interfaces.Importer import Importer
from .monitors import JsonMonitor

if TYPE_CHECKING:
    from uptime.ApiClient import ApiClient


class RemoteJsonImporter(Importer):

    def __init__(self, api: 'ApiClient'):
        super().__init__(api)
        self.url = os.getenv('REMOTE_JSON_URL')

    def load_data_source(self):
        print(f'Fetching monitors from {self.url}')
        response = requests.get(self.url)
        response.raise_for_status()
        items = response.json()

        for item in items:
            self._add_monitor(
                JsonMonitor({'friendly_name': item['domain']}, self.api)
            )

        print(f'Fetched {len(self.monitors)} monitors from remote JSON.')

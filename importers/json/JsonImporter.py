import json
from typing import Dict, Any, TYPE_CHECKING
from importers.interfaces.Importer import Importer
from .monitors import JsonMonitor

if TYPE_CHECKING:
    from uptime.ApiClient import ApiClient


class JsonImporter(Importer):

    def __init__(self, api: 'ApiClient'):
        super().__init__(api)

    def load_data_source(self):
        with open('json_data/domains.json', 'r') as f:
            items = json.load(f)

        for item in items:
            self._add_monitor(
                JsonMonitor({'friendly_name': item['domain']}, self.api)
            )

        print(f'Fetched {len(self.monitors)} monitors from JSON file.')

import os
import json
import requests
from typing import Dict, Any, TYPE_CHECKING
from importers.interfaces.Importer import Importer
from importers.interfaces.Monitor import Monitor
from .monitors import UptimeRobotHttpMonitor, UptimeRobotKeywordMonitor, UptimeRobotPingMonitor, UptimeRobotPortMonitor

if TYPE_CHECKING:
    from uptime.ApiClient import ApiClient


class UptimeRobotImporter(Importer):
    def __init__(self, api: 'ApiClient'):
        super().__init__(api)
        self.uptimerobot_url = os.getenv('UPTIMEROBOT_URL')
        self.uptimerobot_api_key = os.getenv('UPTIMEROBOT_API_KEY')
        self.uptimerobot_offset = int(os.getenv('UPTIMEROBOT_OFFSET', '0'))

    def load_data_source(self):
        print('Fetching monitors from UptimeRobot API.')
        offset = self.uptimerobot_offset
        limit = 50
        fetched_monitors = []

        while True:
            batch = self._fetch_batch(offset=offset, limit=limit)
            if not batch:
                break
            fetched_monitors.extend(batch)
            print(f'Fetched {len(batch)} monitors (total: {len(fetched_monitors)})')
            if len(batch) < limit:
                break
            offset += limit

        for raw in fetched_monitors:
            self._add_monitor(self._get_monitor(raw))

        print(f'Fetched {len(self.monitors)} monitors total from UptimeRobot API.')

    def _fetch_batch(self, offset: int, limit: int) -> list:
        payload = (
            f"api_key={self.uptimerobot_api_key}"
            f"&format=json&logs=1"
            f"&offset={offset}&limit={limit}"
        )
        headers = {
            'content-type': 'application/x-www-form-urlencoded',
            'cache-control': 'no-cache',
        }
        response = requests.post(self.uptimerobot_url, data=payload, headers=headers)
        data = response.json()
        if data['stat'] != 'ok':
            raise Exception(f"UptimeRobot API error: {data}")
        return data['monitors']

    def _get_monitor(self, raw: Dict[str, Any]) -> Monitor:
        monitor_classes = {
            1: UptimeRobotHttpMonitor,
            2: UptimeRobotKeywordMonitor,
            3: UptimeRobotPingMonitor,
            4: UptimeRobotPortMonitor,
        }
        cls = monitor_classes.get(raw['type'])
        if not cls:
            raise ValueError(f"Unsupported UptimeRobot monitor type: {raw['type']}")
        return cls(raw, self.api)

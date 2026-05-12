import os
from abc import ABC, abstractmethod
from uptime.ApiClient import ApiClient


class Importer(ABC):

    def __init__(self, api: ApiClient):
        self.api = api
        self.skip_paused_monitors = os.getenv('SKIP_PAUSED_MONITORS', '').upper() == 'TRUE'
        self.monitors = []
        self._seen_names: set[str] = set()

    def _add_monitor(self, monitor) -> bool:
        if monitor.name in self._seen_names:
            print(f"Monitor '{monitor.name}' is a duplicate in source data and will be skipped.")
            return False
        self._seen_names.add(monitor.name)
        self.monitors.append(monitor)
        return True

    @abstractmethod
    def load_data_source(self):
        pass

    def migrate(self):
        existing_names = self.api.get_existing_names()
        for monitor in self.monitors:
            if monitor.name in existing_names:
                print(f"Monitor '{monitor.name}' already exists in Uptime Kuma.")
                continue
            if self.skip_paused_monitors and monitor.status == 0:
                print(f"Monitor '{monitor.name}' is paused and will be skipped.")
                continue
            monitor.migrate()

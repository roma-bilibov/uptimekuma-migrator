import os, json
from importers.interfaces.Importer import Importer
from importers.interfaces.Monitor import Monitor
from .monitors import JsonMonitor

class JsonImporter(Importer):

    def __init__(self, api: ApiClient):
        super().__init__(api)


    def load_data_source(self):
        with open('json_data/domains.json', 'r') as file:
            items = json.load(file)

        for item in items:
            self.monitors.append(
                self._getMonitor(item)
            )

        print(f'Fetched {len(self.monitors)} monitors total from UptimeRobot API.')

    
    def _getMonitor(self, fetched_monitor: Dict[str, Any]) -> Monitor:
        return JsonMonitor({
            'friendly_name': fetched_monitor['domain']
        }, self.api)

  
    # Sync monitor to Uptime Kuma API
    def migrate(self):
        """
        Syncs a monitors to Uptime Kuma API.
        """
        for i, monitor in enumerate(self.monitors, 1):
            # Check if monitor already exists in Uptime Kuma
            if self.api.check_if_monitor_exists(monitor):
                print(f"Monitor '{monitor.name}' already exists in Uptime Kuma.")
                continue

            # Skip paused monitors
            if self.skip_paused_monitors and monitor.status == 0:
                print(f"Monitor '{monitor.name}' is paused and will be skipped.")
                continue

            monitor.migrate()
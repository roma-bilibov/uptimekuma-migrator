import os
from uptime_kuma_api import UptimeKumaApi
from importers.interfaces.Monitor import Monitor

_REQUIRED_VARS = ['UPTIME_API_URL', 'UPTIMEKUMA_USERNAME', 'UPTIMEKUMA_PASSWORD', 'CLEAN_EXISTING_MONITORS', 'SKIP_PAUSED_MONITORS']

class ApiClient:
    def __init__(self):
        missing = [v for v in _REQUIRED_VARS if not os.getenv(v)]
        if missing:
            raise EnvironmentError(f"Missing required env vars: {', '.join(missing)}")

        self.api = UptimeKumaApi(os.getenv('UPTIME_API_URL'))
        self.api.login(os.getenv('UPTIMEKUMA_USERNAME'), os.getenv('UPTIMEKUMA_PASSWORD'))
        self._clean_if_configured()

    def disconnect(self):
        self.api.disconnect()

    def get_existing_names(self) -> set[str]:
        return {m['name'] for m in self.api.get_monitors()}

    def add_monitor(self, **kwargs):
        self.api.add_monitor(**kwargs)

    def _clean_if_configured(self):
        if os.getenv('CLEAN_EXISTING_MONITORS', '').upper() != 'TRUE':
            return
        confirm = input('This will delete ALL existing monitors from Uptime Kuma. Are you sure? [y/N]: ').strip().lower()
        if confirm != 'y':
            print('Skipping monitor cleanup.')
            return
        print('Cleaning monitors from Uptime Kuma API.')
        for monitor in self.api.get_monitors():
            self.api.delete_monitor(monitor['id'])
            print(f"Monitor '{monitor['name']}' deleted from Uptime Kuma.")
        print('Done cleaning monitors from Uptime Kuma API.')

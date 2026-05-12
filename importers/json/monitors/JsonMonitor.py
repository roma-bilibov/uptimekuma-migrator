import os
from typing import Dict, Any, TYPE_CHECKING
from uptime_kuma_api import MonitorType, UptimeKumaException
from importers.interfaces.Monitor import Monitor

if TYPE_CHECKING:
    from uptime.ApiClient import ApiClient


class JsonMonitor(Monitor):
    def __init__(self, monitor: Dict[str, Any], api: 'ApiClient'):
        super().__init__(monitor, api)
        self.url = f'https://{self.name}'
        self.interval = int(os.getenv('MONITOR_INTERVAL', '20'))
        self.status = 1
        self.expire_notification = os.getenv('EXPIRE_NOTIFICATION', '0')

    def migrate(self):
        try:
            self.api.add_monitor(
                type=MonitorType.HTTP,
                name=self.name,
                url=self.url,
                hostname=self.url,
                interval=self.interval,
                expiryNotification=self.expire_notification,
                accepted_statuscodes=self.accepted_statuscodes
            )
            print(f"Monitor '{self.name}' added to Uptime Kuma with type HTTP.")
        except UptimeKumaException as e:
            print(f"Monitor '{self.name}' failed to sync to Uptime Kuma.")
            print(e)

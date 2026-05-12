import os
from uptime_kuma_api import MonitorType
from importers.interfaces.Monitor import Monitor
from uptime_kuma_api import UptimeKumaException
from typing import Dict, Any, Optional
from uptime.ApiClient import ApiClient

class UptimeRobotHttpMonitor(Monitor):
    def __init__(
        self,
        monitor: Dict[str, Any],
        api: ApiClient
    ):
        super().__init__(monitor, api)
        self.expire_notification = os.getenv('EXPIRE_NOTIFICATION')


    def migrate(self):
        try:
            self.api.add_monitor(
                type=MonitorType.HTTP,
                name=self.name,
                url=self.monitor['url'],
                hostname=self.monitor['url'],
                interval=self.monitor['interval'],
                expiryNotification=self.expire_notification,
            )
            
            print(f"Monitor '{self.name}' added to Uptime Kuma with type HTTP.")

        except UptimeKumaException as e:
            print(f"Monitor '{self.name}' failed to sync to Uptime Kuma.")
            print(e)
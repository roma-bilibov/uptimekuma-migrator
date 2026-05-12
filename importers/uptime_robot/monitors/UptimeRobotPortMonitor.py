from uptime_kuma_api import MonitorType
from importers.interfaces.Monitor import Monitor
from uptime_kuma_api import UptimeKumaException
from typing import Dict, Any, Optional
from uptime.ApiClient import ApiClient

class UptimeRobotPortMonitor(Monitor):
    def __init__(
        self,
        monitor: Dict[str, Any],
        api: ApiClient
    ):
        super().__init__(monitor, api)


    def migrate(self):
        try:
            self.api.add_monitor(
                type=MonitorType.PORT,
                name=self.name,
                url=self.monitor['url'],
                interval=self.monitor['interval'],
                hostname=self.monitor['url'],
                port=self.monitor['port'],
                accepted_statuscodes=self.accepted_statuscodes
            )
            print(f"Monitor '{self.name}' added to Uptime Kuma with type PORT.")

        except UptimeKumaException as e:
            print(f"Monitor '{self.name}' failed to sync to Uptime Kuma.")
            print(e)
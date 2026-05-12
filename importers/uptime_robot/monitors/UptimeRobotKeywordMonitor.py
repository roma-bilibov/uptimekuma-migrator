from uptime_kuma_api import MonitorType
from importers.interfaces.Monitor import Monitor
from uptime_kuma_api import UptimeKumaException
from typing import Dict, Any, Optional
from uptime.ApiClient import ApiClient

class UptimeRobotKeywordMonitor(Monitor):
    def __init__(
        self,
        monitor: Dict[str, Any],
        api: ApiClient
    ):
        super().__init__(monitor, api)


    def migrate(self):
        try:
            if self.monitor['keyword_type'] == 1:
                flip = True
            else:
                flip = False

            self.api.add_monitor(
                type=MonitorType.KEYWORD,
                name=self.name,
                url=self.monitor['url'],
                hostname=self.monitor['url'],
                interval=self.monitor['interval'],
                keyword=self.monitor['keyword_value'],
                upsideDown=flip,
                accepted_statuscodes=self.accepted_statuscodes
            )

            print(f"Monitor '{self.name}' added to Uptime Kuma with type KEYWORD.")

        except UptimeKumaException as e:
            
            print(f"Monitor '{self.name}' failed to sync to Uptime Kuma.")
            print(e)
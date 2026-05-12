import os, json, requests
from importers.interfaces.Importer import Importer
from importers.interfaces.Monitor import Monitor
from .monitors import UptimeRobotHttpMonitor, UptimeRobotKeywordMonitor, UptimeRobotPingMonitor, UptimeRobotPortMonitor

class UptimeRobotImporter(Importer):
    def __init__(self, api: ApiClient):
        super().__init__(api)

        # UptimeRobot
        self.uptimerobot_monitor_url = os.getenv('UPTIMEROBOT_URL')  # your UptimeRobot URL
        self.uptimerobot_api_key = os.getenv('UPTIMEROBOT_API_KEY')  # your UptimeRobot API key
        self.uptimerobot_offset = int(os.getenv('UPTIMEROBOT_OFFSET'))



    def load_data_source(self):
        """Fetch all monitors from UptimeRobot API and sync them to Uptime Kuma."""
        
        # Fetch all monitors with pagination
        print('Fetching monitors from UptimeRobot API.')
        offset = getattr(self, 'uptimerobot_offset', 0)
        limit = 50  # API limit per request
        fetched_monitors = []
        
        while True:
            monitors = self._fetch_uptimerobot_monitors(offset=offset, limit=limit)
            
            if not monitors:
                break
                
            fetched_monitors.extend(monitors)
            print(f'Fetched {len(monitors)} monitors (total: {len(fetched_monitors)})')
            
            # If we got fewer than the limit, we've reached the end
            if len(monitors) < limit:
                break
                
            offset += limit
            self.uptimerobot_offset = offset
            print(f'Fetching next batch with offset {offset}...')

        
        for fetched_monitor in fetched_monitors:
            self.monitors.append(
                self._getMonitor(fetched_monitor)
            )
        
        print(f'Fetched {len(self.monitors)} monitors total from UptimeRobot API.')

    
    # Fetch monitors from UptimeRobot API
    def _fetch_uptimerobot_monitors(self, offset=0, limit=50):
        """
        Fetches monitor data from UptimeRobot API.
        Returns a list of monitors.
        """
        payload = f"api_key={self.uptimerobot_api_key}&format=json&logs=1&offset={self.uptimerobot_offset}"
        headers = {
            'content-type': "application/x-www-form-urlencoded",
            'cache-control': "no-cache"
        }
        response = requests.request("POST", self.uptimerobot_monitor_url, data=payload, headers=headers)
        data = json.loads(response.text)

        if data['stat'] == 'ok':
            return data['monitors']
        else:
            raise Exception('Failed to fetch monitors from UptimeRobot API.')

    
    def _getMonitor(self, fetched_monitor: Dict[str, Any]) -> Monitor:
        monitors = {
            1: UptimeRobotHttpMonitor,    # HTTP
            2: UptimeRobotKeywordMonitor, # KEYWORD
            3: UptimeRobotPingMonitor,    # PING
            4: UptimeRobotPortMonitor,    # PORT
        }

        monitor_class = monitors.get(fetched_monitor['type'])
        if not monitor_class:
            raise ValueError(f"Unsupported UptimeRobot monitor: {type}. \nAvailable monitors: 1.HTTP, \n2. Keyword, \n3.Ping, \n4.Port")
        
        return monitor_class(fetched_monitor, self.api)

  
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
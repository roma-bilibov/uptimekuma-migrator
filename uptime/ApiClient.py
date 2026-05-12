import os 
from uptime_kuma_api import UptimeKumaApi
from importers.interfaces.Monitor import Monitor

class ApiClient:
    def __init__(self):
        # Your details
        uptimekuma_api_url = os.getenv('UPTIME_API_URL')  # domain or IP address of your Uptime Kuma instance
        uptimekuma_username = os.getenv('UPTIMEKUMA_USERNAME')  # your Uptime Kuma username
        uptimekuma_password = os.getenv('UPTIMEKUMA_PASSWORD')  # your Uptime Kuma password     

        # Uptime Kuma API login
        self.api = UptimeKumaApi(uptimekuma_api_url)
        self.api.login(uptimekuma_username, uptimekuma_password)

        self.clean_uptimekuma_monitors()

    
    # Clean monitors from Uptime Kuma API
    def clean_uptimekuma_monitors(self):
        if os.getenv('CLEAN_EXISTING_MONITORS').upper() == 'TRUE':
            """
            Cleans monitors from Uptime Kuma API.
            """
            print('Cleaning monitors from Uptime Kuma API.')
            monitors = self.api.get_monitors()
            for monitor in monitors:
                self.api.delete_monitor(monitor['id'])
                print(f"Monitor '{monitor['name']}' deleted from Uptime Kuma.")
            print('Done cleaning monitors from Uptime Kuma API.')


    def check_if_monitor_exists(self, monitor: Monitor):
        """
        Checks if a monitor already exists in Uptime Kuma.
        Returns True if monitor exists, False if not.
        """
        monitors = self.api.get_monitors()
        for m in monitors:
            if m['name'] == monitor.name:
                return True
        return False


    def add_monitor(self, **kwargs):
        self.api.add_monitor(**kwargs)
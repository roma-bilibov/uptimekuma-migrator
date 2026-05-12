import os
from abc import ABC, abstractmethod
from typing import Dict, Any
from uptime.ApiClient import ApiClient


class Importer(ABC):

    def __init__(
        self,
        api: ApiClient
    ):
        self.api = api
        self.skip_paused_monitors = os.getenv('SKIP_PAUSED_MONITORS').upper() == 'TRUE'
        self.monitors = []
    

    @abstractmethod
    def load_data_source(self):
        """Load Monitors data from source."""
        pass


    @abstractmethod
    def migrate(self):
        """ Import Monitors into Uptime Kuma."""
        pass
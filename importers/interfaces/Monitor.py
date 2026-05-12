from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, TYPE_CHECKING
from enum import IntEnum
import os, json

if TYPE_CHECKING:
    from uptime.ApiClient import ApiClient


class Monitor(ABC):    

    def __init__(
        self,
        monitor: Dict[str, Any],
        api: 'ApiClient'
    ):
        self.monitor = monitor
        self.api = api
        self.name = monitor['friendly_name'].strip()
        self.status = int(monitor['status']) if 'status' in monitor else 0
        self.accepted_statuscodes = json.loads(os.getenv('ACCEPTED_STATUSCODES', '[]'))
    

    @abstractmethod
    def migrate(self):
        """Pushes Monitor to Uptime Kuma"""
        pass